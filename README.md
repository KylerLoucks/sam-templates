# HUB for everything SAM

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li>
      <a href="#best-practices">Best Practices</a>
      <ul>
        <li><a href="#use-aws-lambda-powertools">Use aws-lambda-powertools</a></li>
        <li><a href="#use-lambda-layers-to-enforce-dry-code-standards">Use Lambda Layers to enforce DRY code standardss</a></li>
        <li><a href="#configure-vscodelaunchjson-for-debugging-locally">Configure .vscode/launch.json for debugging locally</a></li>
        <li><a href="#cost-optimization">Cost Optimization</a></li>
      </ul>
    <li><a href="#deploying">Deploying</a></li>
    </li>
  </ol>
</details>

# Getting Started
## Prerequisites
* [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
* [VSCode](https://code.visualstudio.com/download)
* [Docker](https://docs.docker.com/get-docker/)
* [AWS Toolkit VSCode Extension](https://marketplace.visualstudio.com/items?itemName=AmazonWebServices.aws-toolkit-vscode)
* [AWS CLI with IAM credentials configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)


# Best Practices

## Use [aws-lambda-powertools](https://docs.powertools.aws.dev/lambda/python/latest/)

Powertools can be installed using the following command:
```bash
pip install aws-lambda-powertools
```


1. Add the `@logger.inject_lambda_context(log_event=True)` decorator for your lambda handler to include the event in the function logs without having to explicitly define a log entry in the code.

2. Add the `@tracer.capture_lambda_handler` decorator to be able to capture and send data to X-Ray like latency between services like S3, and troubleshoot potential bottlenecks in your code.

```py
from aws_lambda_powertools import Tracer, Logger
tracer = Tracer()
logger = Logger()

# GOOD
@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True) # Use this to stop manually logging events in every function
def lambda_handler(event, context):
    ...


# BAD
def lambda_handler(event, context):
    logger.info(event)
```



3. Add `Service Name` parameter when initializing loggers
```py
from aws_lambda_powertools import Logger
logger = Logger(service="MyModuleServiceName")
```
This name can help differentiate logs coming from different parts of the application or different microservices in a larger architecture.


## Use Lambda Layers to enforce DRY code standards
1. Create layer(s) for code that is used frequently between lambda functions

### Layer folder structure example:
```
template.yml
layers
└── commoncode
    ├── __init__.py
    ├── util.py
    ├── requirements.txt # <- use for additional dependencies

```
### Template.yml:
```yml
Resources:
  # Layer for the Python based lambdas
  PythonLayer:
    Type: AWS::Serverless::LayerVersion
    Metadata:
      BuildMethod: python3.10
      BuildArchitecture: x86_64
    Properties:
      LayerName: common-code-layer
      Description: DRY code Layer used across Lambda functions
      ContentUri: layers/commoncode # See folder structure above
      CompatibleArchitectures:
        - x86_64
      CompatibleRuntimes:
        - python3.10
        - python3.9
```


2. Add the following lines to `.vscode/settings.json`
```json
{
    "python.analysis.extraPaths": ["${workspaceFolder}/path/to/your-layer-folder"]
}
```
> This will allow you to see intellisense for common code you package as a layer.
To verify, start typing your python module followed by `Ctrl+Space` to see a list of functions/classes in your module.



## Configure `.vscode/launch.json` for debugging locally
> [!NOTE] 
`AWS Toolkit VSCode extension` and `Docker` are Both Required.


Edit `.vscode/launch.json` config file to look like the following (Replacing the `body` json block with the payload you want to pass to your lambda function):

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
                "templatePath": "${workspaceFolder}/path/to/template.yml",
                "logicalId": "myLambda" // <- Replace with the resource id in the "Resources" block of the template file.
            },
            "lambda": {
                "runtime": "python3.10", // Replace runtime accordingly
                "payload": {
                    "json": {
                        "Records": [
                            {
                                "body": {} // Replace body/Records blocks accordingly
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

You can also specify a path to a json file instead. For example:
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
                "templatePath": "${workspaceFolder}/path/to/template.yml",
                "logicalId": "myLambda" // <- Replace with the resource id in the "Resources" block of the template file.
            },
            "lambda": {
                "runtime": "python3.10", // Replace runtime accordingly
                "payload": {
                    "path": "${workspaceFolder}/events/example-payload.json" // <- Path to .json file
                },
                "environmentVariables": { "ENV_KEY": "value"}
            }
        },
    ]
}
```

### Running the code locally
1. Open VsCode, Select `Run and Debug (Ctrl + Shift + D)`
2. Select the `RUN AND DEBUG` dropdown and select the config name e.g. `myLambdaFunctionInvoke`
3. Place debug breakpoints in the respective function
4. Run the debugger by selecting the green arrow or by pressing `[F5]`


### Running the code locally w/o debugger
If you don't need to use the debugger, you can simply run the following command to invoke your lambda function (replace `MyFunction` with the logicalId defined in your template.yml)
```bash
sam local invoke MyFunction -e events/example-payload.json
```

## Cost Optimization
You can run [AWS Lambda Power Tuning](https://docs.aws.amazon.com/lambda/latest/operatorguide/profile-functions.html) against your lambda functions to determine which `MemorySize` and `Architecture` configuration will provide the optimal cost/performance ratio.

>Instructions on deploying and testing this can be found [here](https://github.com/alexcasalboni/aws-lambda-power-tuning)


### Migrating x86 Lambda functions to arm64
Many Lambda functions may only need a configuration change to take advantage of the price/performance of Graviton2. Other functions may require repackaging the Lambda function using Arm-specific dependencies, or rebuilding the function binary or container image.

You may not require an Arm processor on your development machine to create Arm-based functions. You can build, test, package, compile, and deploy Arm Lambda functions on x86 machines using `AWS SAM` and `Docker Desktop`. If you have an Arm-based system, such as an `Apple M1 Mac`, you can natively compile binaries.
> More information can be found in [this post](https://aws.amazon.com/blogs/compute/migrating-aws-lambda-functions-to-arm-based-aws-graviton2-processors/)


### x86_64:
For Memory intensive Lambdas, it is most cost effective to use x86_64 architecture.
For CPU intensive workloads, ARM64 provides the quickest execution times and most cost savings over x86_64.

### arm64:
To build Lambda functions using `arm64` architecture on Linux and Windows, use the following command:
```bash
sam build -u
```
> The `-u` or `--use-container` flag will tell SAM to build the function inside a docker container using an image appropriate for the architecture the lambda runs on.

If the build process hangs, enable the `multiarchitecture` setting for docker by running this command:
```docker
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
```


> More details on arm64 vs x86_64 pros/cons are explained in [this post](https://aws.amazon.com/blogs/apn/comparing-aws-lambda-arm-vs-x86-performance-cost-and-analysis-2/)




# Deploying

```
sam build
```

```
sam deploy --config-env <environment>
```
