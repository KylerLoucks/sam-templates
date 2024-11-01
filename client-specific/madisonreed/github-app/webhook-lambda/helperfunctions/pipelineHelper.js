import { CodePipelineClient, GetPipelineStateCommand, PutApprovalResultCommand } from "@aws-sdk/client-codepipeline";



// Tries to approve a pipelines approval action if it is in progress.
// If the pipeline approval action is not in progress, do nothing
export async function approvePipeline(pipelineName) {
    try {
        const client = new CodePipelineClient();
        // Fetch the current state of the pipeline
        const pipelineState = await client.send(new GetPipelineStateCommand({ name: pipelineName }));
        // Find the specific action state
        // const stage = pipelineState.stageStates.find(stage => stage.stageName === stageName);
        // const action = stage.actionStates.find(action => action.actionName === actionName);
        // const token = action.latestExecution.token;

        // Iterate through stages to find the manual approval action
        for (const stage of pipelineState.stageStates) {
            for (const action of stage.actionStates) {
                // Grab the first action that is in progress that has approval in the name
                if (action.actionName.includes("Approval") && action.latestExecution && action.latestExecution.status === "InProgress") {
                    const token = action.latestExecution.token;

                    // Approve the action
                    const result = await client.send(new PutApprovalResultCommand({
                        pipelineName,
                        stageName: stage.stageName,
                        actionName: action.actionName,
                        result: {
                            summary: "Approval granted by Github App approval action",
                            status: "Approved"
                        },
                        token
                    }));
                    console.log("Pipeline approved successfully:", result);

                    // Update check run? this may not be necessary.


                } else {
                    console.log("No Manual Approval action in progress");
                }
            }
        }
    } catch (error) {
        console.error("Error approving the pipeline:", error);
    }
}

export async function rejectPipeline(pipelineName) {
    try {
        const client = new CodePipelineClient();
        // Fetch the current state of the pipeline
        const pipelineState = await client.send(new GetPipelineStateCommand({ name: pipelineName }));
        
        // Iterate through stages to find the manual approval action
        for (const stage of pipelineState.stageStates) {
            for (const action of stage.actionStates) {
                // Grab the first action that is in progress that has approval in the name
                if (action.actionName.includes("Approval") && action.latestExecution && action.latestExecution.status === "InProgress") {
                    const token = action.latestExecution.token;

                    // Reject the action
                    const result = await client.send(new PutApprovalResultCommand({
                        pipelineName,
                        stageName: stage.stageName,
                        actionName: action.actionName,
                        result: {
                            summary: "Approval rejected by Github App rejection action",
                            status: "Rejected"
                        },
                        token
                    }));
                    console.log("Pipeline rejected successfully:", result);

                } else {
                    console.log("No Manual Approval action in progress");
                }
            }
        }
    } catch (error) {
        console.error("Error rejecting the pipeline:", error);
    }
}