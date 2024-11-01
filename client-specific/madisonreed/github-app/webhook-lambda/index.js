// this is for the lambda function that handles webhook events from Github Apps
import { approvePipeline, rejectPipeline } from "./helperfunctions/pipelineHelper.js";
import { scaleAllEcsServices } from "./helperfunctions/ecsHelper.js";
import { initOctokit } from "./helperfunctions/initializeOctokit.js";
import { updateCheckRun } from "./helperfunctions/checkrunHelper.js";
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
    // console.log(JSON.stringify(event, null, 4));

    const expectedSig = `sha256=${createHmac("sha256", clientSecret).update(event.body).digest("hex")}`;
    const currentSig = event.headers['x-hub-signature-256'];

    if (expectedSig !== currentSig) {
        return {
            statusCode: 401,
            body: JSON.stringify({ message: 'Invalid signature' }),
        };
    }

    const body = JSON.parse(event.body); // parse the stringified body in the event payload
    console.log(JSON.stringify(body, null, 4));
    console.log(`Requested Action: ${body.requested_action.identifier}`);

    // Exit the function execution if it wasn't triggered by a requested_action event (check run button)
    if (!body?.requested_action?.identifier) {
        console.log('No action identifier was specified in this webhook event. Returning...');
        return {
            statusCode: 401,
            body: JSON.stringify({ message: 'No action identifier specified.' }),
        };
    }

    const check_run_id = body.check_run.id;
    const pull_req_id = body.check_run.check_suite.pull_requests[0].number

    const pipeline_name = `pr${pull_req_id}-pipeline`
    const cluster_name = `pr${pull_req_id}-cluster`


    if (body.requested_action.identifier == "approve") {
        await approvePipeline(pipeline_name);
    }

    if (body.requested_action.identifier == "reject") {
        await rejectPipeline(pipeline_name);
    }

    if (body.requested_action.identifier == "hibernate") {
        console.log("Hibernating ECS services.");
        await scaleAllEcsServices(cluster_name, 0);

        await updateCheckRun(
            installationOctokit,
            check_run_id,
            `Ephemeral Pipeline`,
            "completed",
            `Scaled ALL ECS Tasks back to 0`,
            `ECS Tasks are being scaled back to 0`,
            `Mongo, MySQL, Redis, Tophat, ApiServer, and Website are all being scaled back to 0 running tasks.\n [Website](https://pr${pull_req_id}.dev.mdsnrdfd.com)\n [Tophat](https://tophat.pr${pull_req_id}.dev.mdsnrdfd.com)`,
            // Actions
            [
                {"label": "Scale Up", "description": "Scale all ECS service tasks up", "identifier": "scaleup"},
            ],
            "success"
        );
    }

    if (body.requested_action.identifier == "scaleup") {
        await scaleAllEcsServices(cluster_name, 1);
        // update the check run to show different status
        await updateCheckRun(
            installationOctokit,
            check_run_id,
            `Ephemeral Pipeline`,
            "completed",
            `Scaling ALL ECS Tasks up to a running state`,
            `ECS Tasks are being scaled up to 1`,
            'Mongo, MySQL, Redis, Tophat, ApiServer, and Website are all being scaled up to 1 running task.',
            // Actions
            [
                {"label": "Hibernate", "description": "Scale all ECS service tasks to 0", "identifier": "hibernate"},
            ],
            "success"
        );
    }

}



