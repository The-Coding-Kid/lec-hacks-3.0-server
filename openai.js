const { Configuration, OpenAI } = require("openai");
require("dotenv").config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_KEY, // defaults to process.env["OPENAI_API_KEY"]
});

async function main() {
  const chatCompletion = await openai.chat.completions.create({
    messages: [
      {
        role: "user",
        content:
          "Hello World!",
      },
    ],
    model: "gpt-3.5-turbo",
  });

  console.log(chatCompletion.choices[0]);
}

main();