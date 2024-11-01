const AWS = require('aws-sdk');

exports.handler = async (event) => {
    console.info(JSON.stringify(event));
  
    // Key example: 
    // "47b1d158-2a30-4922-b464-f0907ac31718/meeting-events/47b1d158-2a30-4922-b464-f0907ac31718.txt"
   
    const keyInfo = event.Records[0].s3.object.key.split('/');
    
    const id = keyInfo[keyInfo.length - 3]; // 47b1d158-2a30-4922-b464-f0907ac31718
    const keyType = keyInfo[keyInfo.length - 2]; // meeting-events
    const key = event.Records[0].s3.object.key; // full key path
    return;
  };