# Testing Locally
Prerequisites
* SAM CLI
* [VSCode](https://code.visualstudio.com/download)
* [Docker](https://docs.docker.com/get-docker/)
* [AWS Toolkit VSCode Extension](https://marketplace.visualstudio.com/items?itemName=AmazonWebServices.aws-toolkit-vscode)
* [AWS CLI with IAM credentials configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

### launch.json

Edit `.vscode/launch.json` config file to look like the following (Replacing the `body` json block with the payload you want to pass):

```json

{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "aws-sam",
            "request": "direct-invoke",
            "name": "myLambdaFunctionInvoke",
            "invokeTarget": {
                "target": "template",
                "templatePath": "${workspaceFolder}/cicd/slack-notifications/template.yml",
                "logicalId": "myLambda" // <- Replace with the resource id in the "Resources" block of the template file.
            },
            "lambda": {
                "payload": {
                    "json": {
                        "Records": [
                            {
                                "body": {}
                            }
                        ]
                    }
                },
                "environmentVariables": { "ENV_KEY": "value"}
            }
        },

    ]

}
```
## Running the code
1. Open VsCode, Select `Run and Debug (Ctrl + Shift + D)`
2. Select the `RUN AND DEBUG` dropdown and select the config name e.g. `myLambda`
3. Place debug breakpoints in the respective function
4. Run the debugger by selecting the green arrow or by pressing `[F5]`



# Deploying

```
sam build
```

```
sam deploy --config-env <environment>
```