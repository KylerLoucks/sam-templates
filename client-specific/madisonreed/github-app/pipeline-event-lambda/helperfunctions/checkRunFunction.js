export async function updateCheckRun(installationOctokit, check_run_id, name, status, title, summary, text, actions = [], conclusion = null) {
    console.log("PARAMS", check_run_id, name, status, title, summary, text, actions, conclusion);
    const updateChecksPayload = {
        owner: process.env.GITHUB_OWNER,
        repo: process.env.GITHUB_REPO,
        check_run_id,
        name,
        status, // status can be: in_progress, completed, queued. Must provide conclusion if status is completed.
        output: {
            title: title,
            summary: summary,
            text: text,
        //   annotations: [
        //     {
        //       path: '.github/workflows/main.yml',
        //       start_line: 1,
        //       end_line: 1,
        //       annotation_level: 'notice',
        //       message: 'Pipeline started',
        //     },
        //   ],
        },
        actions
    }

    // If the status is "completed", add the conclusion
    if (status === "completed" && conclusion) {
        updateChecksPayload.conclusion = conclusion;
        updateChecksPayload.completed_at = new Date().toISOString(); // Optional: Timestamp for when checkrun was completed
    }
    console.log("UPDATE CHECKS PAYLOAD", updateChecksPayload);
    const response = await installationOctokit.rest.checks.update(updateChecksPayload);
    console.log(JSON.stringify(response, null, 4));
}

export async function createCheckRun(installationOctokit, head_sha, name, status, title, summary, text, actions = []) {
    const updateChecksPayload = {
        owner: process.env.GITHUB_OWNER,
        repo: process.env.GITHUB_REPO,
        head_sha,
        name,
        status, // status can be: in_progress, completed, queued. Must provide conclusion if status is completed.
        output: {
            title: title,
            summary: summary,
            text: text,
        //   annotations: [
        //     {
        //       path: '.github/workflows/main.yml',
        //       start_line: 1,
        //       end_line: 1,
        //       annotation_level: 'notice',
        //       message: 'Pipeline started',
        //     },
        //   ],
        },
        actions
    }

    const {data: response} = await installationOctokit.rest.checks.create(updateChecksPayload);
    console.log(JSON.stringify(response, null, 4));
    return response.id;
}