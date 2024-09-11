import {SSMClient, GetParameterCommand} from "@aws-sdk/client-ssm";
import { CodePipelineClient, GetPipelineExecutionCommand } from "@aws-sdk/client-codepipeline";
import { updateCheckRun, createCheckRun } from "./helperfunctions/checkRunFunction.js";
import { getCheckRunIdForRef } from "./helperfunctions/getCheckRunIdForRef.js";
import { initOctokit } from "./helperfunctions/initializeOctokit.js";

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
const client = new CodePipelineClient();
const appId =  process.env.GITHUB_APP_ID;
const clientId = process.env.GITHUB_CLIENT_ID;
const name = "Ephemeral Pipeline";
const installationOctokit = await initOctokit(appId, privateKey, clientId, clientSecret);

const region = process.env.AWS_REGION;

export const handler = async (event) => {
    console.log(JSON.stringify(event, null, 4));

    // sleep(5000);
    
    try {
        const executionId = event.detail['execution-id'];
        const pipelineName = event.detail.pipeline;
        // prefix is needed for creating URLs to tophat and website (e.g pr17387)
        const pipelineNamePrefix = pipelineName.split("-")[0];
        let commit_message = null;
        let commit_url = null;
        let head_sha = null;

        const command = new GetPipelineExecutionCommand({
            pipelineName: pipelineName,
            pipelineExecutionId: executionId
        });
        const response = await client.send(command);

        // Revision summary isn't included until the Source stage Succeeds
        const artifact_revisions = response.pipelineExecution?.artifactRevisions || [];
        if (artifact_revisions.length > 0) {
            const revision_summary_str = artifact_revisions[0].revisionSummary;
            const revision_summary = JSON.parse(revision_summary_str);
            commit_message = revision_summary.CommitMessage;
            head_sha = artifact_revisions[0].revisionId;
            commit_url = artifact_revisions[0].revisionUrl;
        } else {
            console.log("No artifact revisions found. Skipping this execution...")
            return {
                statusCode: 200,
                body: JSON.stringify({ message: "No artifact revisions found. Skipping this execution..." }),
            };
        }

        const state = event.detail.state;
        const stage = event.detail?.stage || null;
        const action = event.detail?.action || null;
        const checkRunId = await getCheckRunIdForRef(installationOctokit, head_sha, name);

        // Create check run if it doesn't already exist.
        if (!checkRunId) {
            await createCheckRun(
                installationOctokit,
                head_sha,
                name,
                "in_progress",
                "Pipeline Started",
                `Pipeline source succeeded.\n ACTION: ${action}\n STAGE: ${stage}`,
                `Pipeline execution in progress.\n [CodePipeline URL](https://${region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/${pipelineName}/view?region=${region})`
            );
        }
        
        let summaryReason = null;
        const externalExecutionSummary = event.detail['execution-result']?.['external-execution-summary'] || "No summary available. Check CodePipeline Console.";

        switch (event['detail-type']) {
            // Catches when the pipeline fully finishes or any time it fails

            // TODO: Use octokit to grab the pull request id to gather the commit sha and use it during pipeline START event
            // TODO: instead of using "artifact revisions" to gather commit info as its unreliable until the pipeline is fully started.
            case "CodePipeline Pipeline Execution State Change":
                if (state == "FAILED") {
                    summaryReason = externalExecutionSummary;
                    await updateCheckRun(
                        installationOctokit,
                        checkRunId,
                        name,
                        "completed",
                        "Pipeline Failed.",
                        summaryReason,
                        `Pipeline execution failed.\n [CodePipeline URL](https://${region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/${pipelineName}/view?region=${region})`,
                        [],
                        "failure"
                    );
                } else if (state == "SUCCEEDED") {
                    await updateCheckRun(
                        installationOctokit,
                        checkRunId,
                        name,
                        "completed",
                        "Pipeline Succeeded.",
                        "Pipeline run was a success!",
                        `Pipeline execution was succesful.\n [CodePipeline URL](https://${region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/${pipelineName}/view?region=${region})\n [Website](https://${pipelineNamePrefix}.dev.mdsnrdfd.com)\n [Tophat](https://tophat.${pipelineNamePrefix}.dev.mdsnrdfd.com)`,
                        [
                            {"label": "Hibernate", "description": "Scale all ECS service tasks to 0", "identifier": "hibernate"}
                        ],
                        "success"
                    );
                }
                break;

                
            case "CodePipeline Action Execution State Change":
                const category = event.detail.type.category;

                // Commenting this for now since events are not showing in sequential order.
                // if (category === "Source" ) {
                //     if (state === "FAILED") {
                //         const generatedCheckRunId = await createCheckRun(installationOctokit, head_sha, name, "in_progress", "Pipeline Started", `Pipeline source has started. STAGE: ${stage}`, "Pipeline execution in progress");
                //         summaryReason = externalExecutionSummary;
                //         await updateCheckRun(installationOctokit, generatedCheckRunId, name, "completed", "Source Stage Failed", summaryReason, `Pipeline source failed. STAGE: ${stage}`, [], "failure");
                //     } else if (state === "SUCCEEDED") {
                //         await createCheckRun(installationOctokit, head_sha, name, "in_progress", "Pipeline Started", `Pipeline source succeeded.\n STAGE: ${stage}`, "Pipeline execution in progress");
                //     }
                // }

                if (category === "Approval") {
                    if (state === "STARTED") {
                        await updateCheckRun(
                            installationOctokit,
                            checkRunId,
                            name,
                            "in_progress",
                            "Approval Stage Started",
                            "Pipeline approval has started",
                            `Pipeline approval in progress.\n ACTION: ${action}\n STAGE: ${stage}\n [CodePipeline URL](https://${region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/${pipelineName}/view?region=${region})`,
                            [
                                {"label": "Approve", "description": "Approve the pipeline to continue", "identifier": "approve"},
                                {"label": "Reject", "description": "Reject the pipeline to stop", "identifier": "reject"}
                            ]
                        );
                    } else if (state === "FAILED") {
                        summaryReason = externalExecutionSummary;
                        await updateCheckRun(
                            installationOctokit,
                            checkRunId,
                            name,
                            "completed",
                            "Approval Stage Rejected",
                            summaryReason,
                            `Pipeline approval failed.\n ACTION: ${action}\n STAGE: ${stage}\n [CodePipeline URL](https://${region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/${pipelineName}/view?region=${region})`,
                            [],
                            "failure"
                        );
                    } else if (state === "SUCCEEDED") {
                        await updateCheckRun(
                            installationOctokit,
                            checkRunId,
                            name,
                            "in_progress",
                            "Approval Stage Completed",
                            `Pipeline approval has been completed.\n ACTION: ${action}\n STAGE: ${stage}\n [CodePipeline URL](https://${region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/${pipelineName}/view?region=${region})`,
                            "Approval Stage Completed"
                        );
                    }
                }
                
                if (category === "Build") {
                    if (state === "STARTED") {
                        await updateCheckRun(
                            installationOctokit, 
                            checkRunId,
                            name,
                            "in_progress",
                            "Build Stage Started",
                            `Build stage has started for ${action}`,
                            `Pipeline build has started.\n ACTION: ${action}\n STAGE: ${stage}\n [CodePipeline URL](https://${region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/${pipelineName}/view?region=${region})`
                        );
                    } else if (state === "FAILED") {
                        summaryReason = externalExecutionSummary;
                        await updateCheckRun(
                            installationOctokit,
                            checkRunId,
                            name,
                            "completed",
                            "Build Stage Failed",
                            summaryReason,
                            `Build stage failed.\n ACTION: ${action}\n STAGE: ${stage}\n [CodePipeline URL](https://${region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/${pipelineName}/view?region=${region})`,
                            [],
                            "failure"
                        );
                    }
                }
                
                if (category === "Deploy") {
                    if (state === "STARTED") {
                        await updateCheckRun(
                            installationOctokit,
                            checkRunId,
                            name,
                            "in_progress",
                            "Deploy Stage Started",
                            "Deploy stage has started",
                            `Pipeline deploy started.\n ACTION: ${action}\n STAGE: ${stage}\n [CodePipeline URL](https://${region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/${pipelineName}/view?region=${region})`,
                            [
                                {"label": "Approve", "description": "Approve the pipeline to continue", "identifier": "approve"},
                                {"label": "Reject", "description": "Reject the pipeline to stop", "identifier": "reject"}
                            ]
                        );
                    } else if (state === "FAILED") {
                        summaryReason = externalExecutionSummary;
                        await updateCheckRun(
                            installationOctokit,
                            checkRunId,
                            name,
                            "completed",
                            "Deploy Stage Failed",
                            summaryReason,
                            `Pipeline deploy failed.\n ACTION: ${action}\n STAGE: ${stage}\n [CodePipeline URL](https://${region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/${pipelineName}/view?region=${region})`,
                            [],
                            "failure"
                        );
                    }
                }
                break;
            default:
                console.log(`No case for event detail type: ${event['detail-type']}`)
        }
        
        return {
            statusCode: 200,
            body: JSON.stringify({ message: 'GitHub check execution succeeded' }),
        };
        
    } catch (error) {
        console.error('Error:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ message: 'Error executing GitHub check', error: error.message }),
        };
    }
};

function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}