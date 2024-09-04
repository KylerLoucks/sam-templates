# Github App integration with CodePipeline

This code is used to integrate github app check runs with Codepipeline to provide a visual of each pipeline execution and also perform actions from the github UI.


`webhook-lambda` handles the events the github app sends to the specified webhook url. (This should be set to the lambda function URL).

`pipeline-event-lambda` this handles CodePipeline events and creates/updates the checkrun to provide details of the stage that the pipeline is executing.