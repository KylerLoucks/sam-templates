import jwt from "jsonwebtoken";
import { SSMClient, GetParameterCommand } from "@aws-sdk/client-ssm";

const ssm = new SSMClient();
export const handler = async (event) => {
  const getParameter = async (name) => {
    const command = new GetParameterCommand({
      Name: name,
      WithDecryption: true,
    });
    const result = await ssm.send(command);
    return result.Parameter.Value;
  };

  const awsSessionToken = await getParameter("supabasejwt");
  const authorizationHeader =
    event.headers.Authorization || event.headers.authorization;

  if (!authorizationHeader) {
    console.error("No Authorization header found");
    return generatePolicy("user", "Deny", event.methodArn);
  }

  // Extract the token from the Authorization header
  const token = authorizationHeader.replace("Bearer ", "");
  const generatePolicy = (principalId, effect, resource) => {
    const policy = {
      principalId: principalId,
      policyDocument: {
        Version: "2012-10-17",
        Statement: [
          {
            Action: "execute-api:Invoke",
            Effect: effect,
            Resource: resource,
          },
        ],
      },
    };

    return policy;
  };

  try {
    // Verify and decode the JWT'
    const decodedToken = jwt.verify(token, awsSessionToken, {
      algorithms: ["HS256"],
    });

    if (
      decodedToken.aud === "authenticated" &&
      decodedToken.role === "authenticated"
    ) {
      return generatePolicy(decodedToken.sub, "Allow", event.methodArn);
    } else {
      return generatePolicy("user", "Deny", event.methodArn);
    }
  } catch (error) {
    console.error("Error:", error);
    return generatePolicy("user", "Deny", event.methodArn);
  }
};
