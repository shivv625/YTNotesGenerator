const { getTranscript } = require("youtube-transcript");
const axios = require("axios");
const ytdl = require("ytdl-core");

exports.handler = async function (event, context) {
  try {
    if (event.httpMethod !== "POST") {
      return {
        statusCode: 405,
        body: JSON.stringify({ error: "Method Not Allowed" }),
      };
    }

    const { url, style } = JSON.parse(event.body);
    if (!url) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: "Missing YouTube URL" }),
      };
    }

    // 1. Extract transcript
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

    // 2. Extract video metadata
    let metadata = {};
    try {
      const info = await ytdl.getInfo(url);
      metadata = {
        video_title: info.videoDetails.title,
        video_author: info.videoDetails.author.name,
        video_duration: info.videoDetails.lengthSeconds,
        publish_date: info.videoDetails.publishDate,
        view_count: info.videoDetails.viewCount,
        description: info.videoDetails.description,
        video_id: info.videoDetails.videoId,
      };
    } catch (err) {
      metadata = {
        video_title: "",
        video_author: "",
        video_duration: "",
        publish_date: "",
        view_count: "",
        description: "",
        video_id: "",
      };
    }

    // 3. Generate notes using OpenRouter (Mistral)
    const apiKey = process.env.OPENROUTER_API_KEY;
    const prompt = `You are an expert note-taker and educator. Generate ${
      style || "comprehensive"
    } study notes from this YouTube video transcript.\n\nTranscript:\n${transcript}\n\nGenerate ${
      style || "comprehensive"
    }, educational notes in English:`;
    let notes;
    try {
      const response = await axios.post(
        "https://openrouter.ai/api/v1/chat/completions",
        {
          model: "mistralai/mistral-small-3.2-24b-instruct:free",
          messages: [{ role: "user", content: prompt }],
          max_tokens: 1500,
          temperature: 0.7,
        },
        {
          headers: {
            Authorization: `Bearer ${apiKey}`,
            "Content-Type": "application/json",
          },
        }
      );
      notes = response.data.choices[0].message.content;
    } catch (err) {
      return {
        statusCode: 500,
        body: JSON.stringify({
          error: "Failed to generate notes with Mistral AI.",
        }),
      };
    }

    return {
      statusCode: 200,
      body: JSON.stringify({ success: true, notes, ...metadata }),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message }),
    };
  }
};
