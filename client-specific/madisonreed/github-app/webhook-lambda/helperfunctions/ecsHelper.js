import { ECSClient, UpdateServiceCommand, ListServicesCommand } from "@aws-sdk/client-ecs";

// Pass in the ECS cluster name
export async function scaleAllEcsServices(clusterName, desiredCount) {
    const ecsClient = new ECSClient();

    try {
        // List all services under the specified cluster
        const listServicesCommand = new ListServicesCommand({ cluster: clusterName });
        const services = await ecsClient.send(listServicesCommand);

        console.log(JSON.stringify(services));

        // Iterate over each service and scale down to 0
        for (const serviceArn of services.serviceArns) {
            try {
                console.log(`Attempting to scale service ${serviceArn} to ${desiredCount}`);

                const updateServiceCommand = new UpdateServiceCommand({
                    cluster: clusterName,
                    service: serviceArn,
                    desiredCount: desiredCount
                });
    
                const result = await ecsClient.send(updateServiceCommand);
                console.log(`Successfully scaled service: ${serviceArn} to ${desiredCount} tasks, ${result}`);
            } catch (error) {
                console.error(`Error scaling service: ${serviceArn}`, error);
                // Continue the loop even if an error occurs
                continue;
            }
        }
    } catch (error) {
        console.error("Error scaling down services:", error);
        throw error;
    }
}