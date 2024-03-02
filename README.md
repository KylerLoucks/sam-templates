# HUB for everything SAM
Prerequisites
* [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
* [VSCode](https://code.visualstudio.com/download)
* [Docker](https://docs.docker.com/get-docker/)
* [AWS Toolkit VSCode Extension](https://marketplace.visualstudio.com/items?itemName=AmazonWebServices.aws-toolkit-vscode)
* [AWS CLI with IAM credentials configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)


# Best Practices

* Use [aws-lambda-powertools](https://docs.powertools.aws.dev/lambda/python/latest/) package (pip install aws-lambda-powertools)


1. Add the `@logger.inject_lambda_context(log_event=True)` decorator for your lambda handler to include the event in the function logs without having to explicitly define a log entry in the code.

2. Add the `@tracer.capture_lambda_handler` decorator to capture any X-Ray traces to other AWS services. This allows seeing latency between services like S3.

```py
from aws_lambda_powertools import Tracer, Logger
tracer = Tracer()
logger = Logger()

# GOOD
@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True) # Use this to stop manually logging events in every function
def lambda_handler(event, context):
    ...


# BAD
def lambda_handler(event, context):
    logger.info(event)
```



3. Add `Service Name` parameter when initializing loggers
```py
from aws_lambda_powertools import Logger
logger = Logger(service="MyModuleServiceName")
```
This name can help differentiate logs coming from different parts of the application or different microservices in a larger architecture.





* Use Lambda Layers to enforce DRY code standards
1. Create commoncode layer for code that is used frequently between lambda functions

Folder structure example:
```
template.yml
layers
└── commoncode
    ├── __init__.py
    ├── util.py

```
template.yml:
```yml
Resources:
  # Layer for the Python based lambdas
  PythonLayer:
    Type: AWS::Serverless::LayerVersion
    Metadata:
      BuildMethod: python3.10
      BuildArchitecture: x86_64
    Properties:
      LayerName: common-code-layer
      Description: DRY code Layer used across Lambda functions
      ContentUri: layers/commoncode
      CompatibleArchitectures:
        - x86_64
      CompatibleRuntimes:
        - python3.10
        - python3.9
```


2. Add the following lines to `.vscode/settings.json`
```json
{
    "python.analysis.extraPaths": ["${workspaceFolder}/path/to/your-layer-folder"]
}
```
> This will allow you to see intellisense for common code you package as a layer.
To verify, start typing your python module followed by `Ctrl+Space` to see a list of functions/classes in your module.



* Update `.vscode/launch.json` for ease of debugging locally with `AWS Toolkit VSCode extension` and `Docker` (Both Required)


### launch.json

Edit `.vscode/launch.json` config file to look like the following (Replacing the `body` json block with the payload you want to pass to your lambda function):

```json

{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "aws-sam",
            "request": "direct-invoke",
            "name": "myLambdaFunctionInvoke",
            "invokeTarget": {
                "target": "template",
                "templatePath": "${workspaceFolder}/path/to/template.yml",
                "logicalId": "myLambda" // <- Replace with the resource id in the "Resources" block of the template file.
            },
            "lambda": {
                "runtime": "python3.10", // Replace runtime accordingly
                "payload": {
                    "json": {
                        "Records": [
                            {
                                "body": {} // Replace body/Records blocks accordingly
                            }
                        ]
                    }
                },
                "environmentVariables": { "ENV_KEY": "value"}
            }
        },

    ]

}
```
### Running the code
1. Open VsCode, Select `Run and Debug (Ctrl + Shift + D)`
2. Select the `RUN AND DEBUG` dropdown and select the config name e.g. `myLambdaFunctionInvoke`
3. Place debug breakpoints in the respective function
4. Run the debugger by selecting the green arrow or by pressing `[F5]`



# Deploying

```
sam build
```

```
sam deploy --config-env <environment>
```