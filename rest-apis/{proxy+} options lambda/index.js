
/**
 * This function, when used as a {proxy+} resource in the ROOT path of APIGateway, (defined as an OPTIONS method)
 * Will handle all Browser-Initiated Preflight Requests. 
 * 
 * For example, when someone from hackerdomain.com tries to invoke ANY resource path in the API e.g. /docs
 * this OPTIONS function will be invoked and If Preflight Fails: 
 * If the preflight response is a 403 Forbidden or doesn't include the correct CORS headers, 
 * the browser will block the actual request from being made for security reasons. 
 * 
 * 
 * 
 * This makes it so we don't have to specify the HEADERS in the response of all API endpoints (e.g. /docs):
 * /docs response example:
 * return {
 *       statusCode: 200,
 *       headers: {
 *           'Content-Type': 'text/html', <- We no longer have to specify the Allow-Origin or Methods headers like we do in the function below...
 *       },
 *       body: body // Your response body
 * };
 * 
 * 
 * 
 */
exports.handler = async (event) => {
    const origin = event.headers.Origin || event.headers.origin;
    const allowedOrigins = ['mydomain.com', 'my-otherdomain.com'];
    const filteredOrigins = allowedOrigins.filter(o => origin ? origin.endsWith(o) : false);
    if (filteredOrigins && filteredOrigins.length) {
        return {
            statusCode: 200,
            body: 'OK',
            headers: {
                'Access-Control-Allow-Origin': origin,
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Methods': 'GET, POST, PATCH, DELETE',
                'Access-Control-Allow-Headers': 'Content-Type',
            }
        };
    }
    else {
        return {
            statusCode: 403,
            body: ''
        };
    }
}