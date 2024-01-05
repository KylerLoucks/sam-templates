# Testing Locally

### launch.json

```json

{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "aws-sam",
            "request": "direct-invoke",
            "name": "slack-notifications:codePipelineServiceRole",
            "invokeTarget": {
                "target": "template",
                "templatePath": "${workspaceFolder}/cicd/slack-notifications/template.yml",
                "logicalId": "codePipelineServiceRole"
            },
            "lambda": {
                "payload": {},
                "environmentVariables": {}
            }
        },

    ]

}
```

Run and Debug > DropDown > `slack-notifications:codePipelineServiceRole`



# Deploying

```
sam build
```

```
sam deploy --config-env <environment>
```