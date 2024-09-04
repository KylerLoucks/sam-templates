import { ECSClient, UpdateServiceCommand, ListServicesCommand } from "@aws-sdk/client-ecs";

// Pass in the ECS cluster name
export async function scaleAllEcsServices(clusterName, desiredCount) {
    const ecsClient = new ECSClient();

    try {
        // List all services under the specified cluster
        const listServicesCommand = new ListServicesCommand({ cluster: clusterName });
        const services = await ecsClient.send(listServicesCommand);

        // Iterate over each service and scale down to 0
        for (const serviceArn of services.serviceArns) {
            const updateServiceCommand = new UpdateServiceCommand({
                cluster: clusterName,
                service: serviceArn,
                desiredCount: desiredCount
            });

            const result = await ecsClient.send(updateServiceCommand);
            console.log(`Scaled down service: ${serviceArn} to ${desiredCount} tasks, ${result}`);
        }
    } catch (error) {
        console.error("Error scaling down services:", error);
    }
}