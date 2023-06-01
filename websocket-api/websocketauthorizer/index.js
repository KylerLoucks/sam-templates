const CognitoJwtVerifier = require("aws-jwt-verify");

exports.handler = async (event, context, callback) => {
    console.log('Received event:', JSON.stringify(event, null, 2));

    // A simple REQUEST authorizer example to demonstrate how to use request 
    // parameters to allow or deny a request. In this example, a request is  
    // authorized if the client-supplied Authorization header
    // in the request context match the specified values of
    // of 'headerValue1'.

    // Retrieve request parameters from the Lambda function input:
    var headers = event.headers;

       
    // Perform authorization to return the Allow policy for correct parameters and 
    // the 'Unauthorized' error, otherwise.
    
    if (headers.Authorization === "headerValue1") {
        callback(null, generateAllow('me', event.methodArn));
    }  else {
        callback("Unauthorized");
    }
}
    
// Helper function to generate an IAM policy
var generatePolicy = function(principalId, effect, resource) {
    // Required output:
    var authResponse = {};
    authResponse.principalId = principalId;
    if (effect && resource) {
        var policyDocument = {};
        policyDocument.Version = '2012-10-17'; // default version
        policyDocument.Statement = [];
        var statementOne = {
            Effect: effect,
            Action: 'execute-api:Invoke', // default action
            Resource: resource
        };
        policyDocument.Statement[0] = statementOne;
        authResponse.policyDocument = policyDocument;
    }
    // Optional output with custom properties of the String, Number or Boolean type.
    authResponse.context = {
        "stringKey": "stringval",
        "numberKey": 123,
        "booleanKey": true
    };
    return authResponse;
}
    
var generateAllow = function(principalId, resource) {
    return generatePolicy(principalId, 'Allow', resource);
}
    
var generateDeny = function(principalId, resource) {
    return generatePolicy(principalId, 'Deny', resource);
}