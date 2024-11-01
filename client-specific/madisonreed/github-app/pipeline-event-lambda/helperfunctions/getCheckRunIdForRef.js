export async function getCheckRunIdForRef(installationOctokit, commitSha, check_name) {
    try {   
        const listCheckRefPayload = {
            owner: process.env.GITHUB_OWNER,
        repo: process.env.GITHUB_REPO,
        ref: commitSha,
        check_name: check_name
    }

    const {data: response} = await installationOctokit.rest.checks.listForRef(listCheckRefPayload);
        console.log(JSON.stringify(response, null, 4));

        const checkRunId = response.check_runs[0].id

        return checkRunId;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}