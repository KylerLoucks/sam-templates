
import { Octokit, App } from "octokit";

export async function initOctokit(appId, privateKey, clientId, clientSecret) {
    try {
        // Instantiate an instance of the Github app
        const app = new App({
            appId: appId,
            privateKey: privateKey,
            oauth: {
                clientId: clientId,
                clientSecret: clientSecret,
            },
            webhooks: {
                secret: clientSecret
            },
        });

        // Grab installation ID so we can call github rest API as an installation instead of as an App
        const { data: installation } = await app.octokit.request("GET /repos/{owner}/{repo}/installation", {
            owner: process.env.GITHUB_OWNER,
            repo: process.env.GITHUB_REPO,
        });
        const installationOctokit = await app.getInstallationOctokit(installation.id);
        return installationOctokit;

    } catch {
        console.error("Failed to initialize octokit");
    }
}
