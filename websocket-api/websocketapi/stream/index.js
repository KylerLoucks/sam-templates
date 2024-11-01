const { Deepgram } = require("@deepgram/sdk");

const deepgramApiKey = "e73c0ae4b5512db87558989d2babda1b4f085dfd";
const deepgram = new Deepgram(deepgramApiKey);

const AWS = require('aws-sdk');


exports.handler = async (event) => {
    console.info(event)
    
    const domain = event.requestContext.domainName
    const stage = event.requestContext.stage
    const connectionId = event.requestContext.connectionId
    
    console.info("DATA: ", event.body.data)
    
    const deepgramLive = deepgram.transcription.live({
    	punctuate: true,
    // 	interim_results: false,
    	language: "en-US",
    // 	model: "nova",
    });
    
    
    
    deepgramLive.addListener("open", () => {
    	console.log("opened connection with deepgram")
    	deepgramLive.send(event.body.data)
    });
    
    
    deepgramLive.addListener('transcriptReceived', async (data) => {
        console.log("GOT TRANSCRIPTION: ", data)


        // send data back to client
        const api = new AWS.ApiGatewayManagementApi({
            endpoint: `https://${domain}/${stage}`
        });

        const params = {
            ConnectionId: connectionId,
            Data: JSON.stringify(data)
        }

        api.postToConnection(params).promise()
    });

    const response = {
        statusCode: 200,
        body: JSON.stringify('Hello from Lambda!'),
    };
    return response;

};


