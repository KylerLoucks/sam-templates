// this is for the lambda function that handles webhook events from Github Apps
import { approvePipeline, rejectPipeline } from "./helperfunctions/pipelineHelper";
import { scaleAllEcsServices } from "./ecs-helper";
import { initOctokit } from "./helperfunctions/initializeOctokit";
import { updateCheckRun } from "./checkrun-helper";
import { SSMClient, GetParameterCommand } from "@aws-sdk/client-ssm";
import { createHmac } from "crypto";


const ssmClient = new SSMClient(); 

async function getParameterFromStore(parameterName) {
    const command = new GetParameterCommand({
        Name: parameterName,
        WithDecryption: true
    });

    try {
        const response = await ssmClient.send(command);
        return response.Parameter.Value;
    } catch (error) {
        console.error(`Error fetching parameter ${parameterName}:`, error);
        throw error;
    }
}

// Secrets and client Id generated during Github App creation.
const privateKey = await getParameterFromStore("/development/GithubAppPrivateKey");
const clientSecret = await getParameterFromStore("/development/GithubAppSecret");
const appId =  process.env.GITHUB_APP_ID;
const clientId = process.env.GITHUB_CLIENT_ID;

const installationOctokit = await initOctokit(appId, privateKey, clientId, clientSecret);

export const handler = async (event) => {
    console.log(JSON.stringify(event, null, 4));

    const expectedSig = `sha256=${createHmac("sha256", clientSecret).update(event.body).digest("hex")}`;
    const currentSig = event.headers['x-hub-signature-256'];

    if (expectedSig !== currentSig) {
        return {
            statusCode: 401,
            body: JSON.stringify({ message: 'Invalid signature' }),
        };
    }

    const check_run_id = event.body.check_run.id;
    const pull_req_id = event.body.check_run.check_suite.pull_requests[0].number

    const pipeline_name = `pr${pull_req_id}-pipeline`
    const cluster_name = `pr${pull_req_id}-cluster`


    if (event.body.requested_action.identifier == "approve") {
        approvePipeline(pipeline_name);
    }

    if (event.body.requested_action.identifier == "reject") {
        rejectPipeline(pipeline_name);
    }

    if (event.body.requested_action.identifier == "hibernate") {
        scaleAllEcsServices(cluster_name, 0);

        updateCheckRun(
            installationOctokit,
            check_run_id,
            `Ephemeral Pipeline`,
            `Scaled ALL ECS Tasks back to 0`,
            `ECS Tasks are being scaled back to 0`,
            'Mongo, MySQL, Redis, Tophat, ApiServer, and Website are all being scaled back to 0 running tasks.',
            "in_progress", 
            // Actions
            [
                {"label": "Scale Up", "description": "Scale all ECS service tasks up", "identifier": "scaleup"},
            ]
        );
    }

    if (event.body.requested_action.identifier == "scaleup") {
        scaleAllEcsServices(cluster_name, 1);
        // update the check run to show different status
        updateCheckRun(
            installationOctokit,
            check_run_id,
            `Ephemeral Pipeline`,
            `Scaling ALL ECS Tasks up to a running state`,
            `ECS Tasks are being scaled up to 1`,
            'Mongo, MySQL, Redis, Tophat, ApiServer, and Website are all being scaled up to 1 running task.',
            "in_progress", 
            // Actions
            [
                {"label": "Hibernate", "description": "Scale all ECS service tasks to 0", "identifier": "hibernate"},
            ]
        );
    }

}



