
export const handler = async (event, context, callback) => {
    console.info(JSON.stringify(event, null, 4));
    // const body = { msg: "hello world v3"};

    const response = {
      statusCode: 200,
      body: JSON.stringify('Hello from Lambda v12!'),
      // headers: {
      //     'Access-Control-Allow-Headers': 'Authorization',
      //     'Access-Control-Allow-Origin': '*',
      //     'Access-Control-Allow-Methods': 'GET, OPTIONS',
      //     'Access-Control-Allow-Credentials': 'true',
      // },
      // "isBase64Encoded": false
    };

    return response;
};