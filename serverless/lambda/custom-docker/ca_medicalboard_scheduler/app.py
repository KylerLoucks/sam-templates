import ftplib
import re
import datetime
from pathlib import Path
import zipfile
import os
import shutil
import subprocess
import boto3
from botocore.exceptions import ClientError
import logging

dynamodb = boto3.client('dynamodb')
table_name = os.environ['DATASET_INFO_TABLE']
bucket_name = os.environ['DATA_BUCKET']
ftp_pass_key_param = os.environ['FTP_PASS_KEY_PARAM']
ftp_address = os.environ['FTP_ADDRESS']
FTP_USER = "PoLYviEW3"


ssm_client = boto3.client('ssm')
response = ssm_client.get_parameter(Name=ftp_pass_key_param, WithDecryption=True)
FTP_PASS = response['Parameter']['Value']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    directory = 'MBC'
    local_save_path = '/tmp/'
    dataset_updated = download_latest_zip(ftp_address, directory, local_save_path)
    return {
        'statusCode': 200,
        'body': 'Success',
        'datasetUpdated': dataset_updated
    }

def check_ftp_file_exists(ftp, filename):
    """
    Check if a file exists in the FTP server.
    """
    try:
        ftp.size(filename)  # If this doesn't cause an error, the file exists
        return True
    except ftplib.error_perm:
        return False
    
def generate_filename(date):
    return f"MBCPhysicianAndSurgeonInformation-PUBLIC-{date.strftime('%Y%m%d')}.zip"


def download_latest_zip(ftp_address, directory, local_save_path, days_limit=30):
    # Check DynamoDB for the last file that was downloaded
    item = get_last_downloaded_file(provider="California")
    last_downloaded_file = ""
    if item:
        last_downloaded_file = item['file']['S']
    
    with ftplib.FTP(ftp_address) as ftp:
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        ftp.cwd(directory)

        date = datetime.date.today()
        end_date = date - datetime.timedelta(days=days_limit)

        while date >= end_date:
            filename = generate_filename(date)

            # Check if the filename matches the most recent file we downloaded previously
            if filename == last_downloaded_file:
                logger.info("The most recent data has already been downloaded. S3 contains the lastest data!")
                return False

            if check_ftp_file_exists(ftp, filename):
                logger.info(f"Found the latest data: {filename}")
                tmp_file_path = Path(local_save_path) / filename
                with open(tmp_file_path, 'wb') as f:
                    ftp.retrbinary(f'RETR {filename}', f.write)
                logger.info(f"Downloaded {filename} to {tmp_file_path}")

                # Unzip the Dataset
                extracted_path = Path(tmp_file_path.parent, "extracted")
                with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
                    zip_ref.extractall(extracted_path)
                    logger.info(f"Extracted dataset zip file to: {extracted_path}")

                # Export the accdb file to .csv files
                accdb_file_path = find_accdb_file(extracted_path)
                if accdb_file_path:
                    logger.info(f".accdb file found in path: {accdb_file_path}")
                    accdb_convert_to_csv(accdb_file_path)
                else:
                    raise FileNotFoundError("No .accdb file found in the extracted data.")

                # Upload the CSV files to S3
                output_dir = Path(accdb_file_path).parent / (Path(accdb_file_path).stem + '_csv')
                for csv_file in os.listdir(output_dir):
                    if csv_file.startswith("REF_"):
                        # Upload the REF_ files to the REFS folder 
                        upload_to_s3(bucket_name, f"MedicalBoards/California/REFS/{csv_file}", str(output_dir / csv_file))
                        logger.info(f"Uploaded REF file: {csv_file} to S3 path: {bucket_name}/MedicalBoards/California/REFS/{csv_file}")
                    else:
                        # Upload the non REF_ files to the Dataset folder
                        upload_to_s3(bucket_name, f"MedicalBoards/California/Dataset/{csv_file}", str(output_dir / csv_file))
                        logger.info(f"Uploaded Dataset file: {csv_file} to S3 path: {bucket_name}/MedicalBoards/California/Dataset/{csv_file}")

                # Write to DynamoDB the latest file that was downloaded
                update_last_downloaded_file(provider="California", filename=filename)
                
                # Remove /tmp/extracted and /tmp/MBCPhysicianAndSurgeonInformation-PUBLIC-<date>.zip
                shutil.rmtree(extracted_path)
                os.remove(tmp_file_path)

                return True
            date -= datetime.timedelta(days=1)

        logger.info("No ZIP files found within the specified date range.")


def upload_to_s3(bucket_name, s3_path, local_file):
    s3 = boto3.client('s3')
    s3.upload_file(local_file, bucket_name, s3_path)

def find_accdb_file(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".accdb"):
                return os.path.join(root, file)
    return None


def accdb_convert_to_csv(accdb_file_path):
    # Extract file name and directory from the provided path
    file_name = os.path.basename(accdb_file_path)
    file_path = os.path.dirname(accdb_file_path)

    # Construct the output directory
    output_dir = os.path.join(file_path, file_name.split('.')[0] + '_csv')
    
    # Create the output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the list of table names
    result = subprocess.run(["mdb-tables", "-1", accdb_file_path], capture_output=True, text=True)
    tables = result.stdout.splitlines()
    
    # Loop through each table and export it to CSV
    for table in tables:
        logger.info(f"Extracting Microsoft Access Table: '{table}' to CSV")
        csv_file_path = os.path.join(output_dir, f"{table}.csv")
        
        with open(csv_file_path, "w") as csv_file:
            subprocess.run(["mdb-export", accdb_file_path, table], stdout=csv_file)

# Grab last url that was used to pull data from Dynamo
def get_last_downloaded_file(provider):
    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key={'provider': {'S': provider}}
        )
        item = response.get('Item', {})
        if not item:
            logger.info(f"Dynamo returned zero items for provider '{provider}'")
            return None
        return item
    except ClientError as e:
        logger.error(f"An error occurred: couldn't find dynamodb record for {provider}, {e.response['Error']['Message']}")
        return None
    
def update_last_downloaded_file(provider, filename):
    try:
        response = dynamodb.update_item(
            TableName=table_name,
            Key={'provider': {'S': provider}},
            UpdateExpression="SET #file = :file",
            ExpressionAttributeNames={
                '#file': "file"
            },
            ExpressionAttributeValues={
                ':file': {"S": filename},
            },
        )
        logger.info(f"Updated DynamoDB provider record: '{provider}' with file: {filename}")
        return response
    except ClientError as e:
        logger.error(f"Couldn't update last url used: {e.response['Error']['Message']}")
        return None


