const { CognitoJwtVerifier } = require("aws-jwt-verify");
const userPoolId = process.env.USERPOOL_ID
const clientId = process.env.USERPOOL_CLIENT_ID

exports.handler = async (event, context, callback) => {
    console.log('Received event:', JSON.stringify(event, null, 2));

    // A REQUEST authorizer that uses request 
    // parameters to allow or deny a request. In this case, a request is  
    // authorized if the client-supplied 'Auth' query string parameter
    // in the request context match a valid JSON web token provided by Cognito.

    // Retrieve request parameters from the Lambda function input:
    const headers = event.headers
    const queryStringParameters = event.queryStringParameters
    const jwtToken = queryStringParameters.Auth;
    console.log("JWT token: ", jwtToken)
       
    // Perform authorization to return the Allow policy for correct parameters and 
    // the 'Unauthorized' error, otherwise.
    
    // Verifier that expects valid access tokens:
    const verifier = CognitoJwtVerifier.create({
      userPoolId: userPoolId,
      tokenUse: "id",
      clientId: clientId,
    });
    
    try {
      const payload = await verifier.verify(jwtToken); // the JWT as string

      console.log("Token is valid. Payload:", payload);
      callback(null, generateAllow('me', event.methodArn));
    } catch (error) {
      console.log("Token not valid!", error);
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