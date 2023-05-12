const { Deepgram } = require("@deepgram/sdk");

const deepgramApiKey = "e73c0ae4b5512db87558989d2babda1b4f085dfd";
const deepgram = new Deepgram(deepgramApiKey);

exports.handler = async (event) => {
    
    console.info(event)
    
    
    
    
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
    
    deepgramLive.addListener('transcriptReceived', (data) => console.log("GOT TRANSCRIPTION: ", data))

    // const socket = new WebSocket('wss://api.deepgram.com/v1/listen', [
    //   'token',
    //   'e73c0ae4b5512db87558989d2babda1b4f085dfd',
    // ])

    const response = {
        statusCode: 200,
        body: JSON.stringify('Hello from Lambda!'),
    };
    return response;

};


