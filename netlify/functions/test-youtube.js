const { getTranscript } = require("youtube-transcript");

exports.handler = async function (event, context) {
  try {
    const url = event.queryStringParameters && event.queryStringParameters.url;
    if (!url) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: "Missing YouTube URL" }),
      };
    }
    let transcriptArr;
    try {
      transcriptArr = await getTranscript(url);
    } catch (err) {
      return {
        statusCode: 400,
        body: JSON.stringify({
          error:
            "Could not retrieve transcript for this video. Subtitles may be disabled.",
        }),
      };
    }
    const transcript = transcriptArr.map((t) => t.text).join(" ");
    return {
      statusCode: 200,
      body: JSON.stringify({ transcript }),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message }),
    };
  }
};
