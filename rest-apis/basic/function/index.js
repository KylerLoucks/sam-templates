const AWS = require('aws-sdk');

exports.handler = async (event) => {
    console.info(JSON.stringify(event));
    const res = {"hello": "world"};
    return {
        statusCode: 200,
        body: JSON.stringify(res),
        headers: {
            'Access-Control-Allow-Headers': 'Authorization',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Credentials': 'true',
          },
    };
  };