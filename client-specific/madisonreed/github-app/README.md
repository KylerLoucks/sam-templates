# Github App integration with CodePipeline

This code is used to integrate github app check runs with Codepipeline to provide a visual of each pipeline execution and also perform actions from the github UI.


`webhook-lambda` handles the events the github app sends to the specified webhook url. (This should be set to the lambda function URL).

`pipeline-event-lambda` this handles CodePipeline events and creates/updates the checkrun to provide details of the stage that the pipeline is executing.

## Prerequisites
1. Create Github App
2. Specify a Webhook URL. This can be an AWS Lambda function URL.
3. Specify a Webhook secret. This just needs to be a secure random string you provide.
4. Give checks:write (read and write) access under `Repository permissions`.
5. Check the box for `Checks` for webhook events you want to listen to.
6. Create the App for `Only on this account`.

7. Note down the App ID and Client ID in the `General` section.
8. Generate a Private key. You'll need to use this .pem key value when instantiating Octokit.
9. Install the App in the specific repository you want to use.