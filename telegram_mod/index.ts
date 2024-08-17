import TelegramBot from "node-telegram-bot-api";
import "dotenv/config";
import Groq from "groq-sdk";

const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const GROQ_API_KEY = process.env.GROQ_API_KEY;

// setup telegram bot
const bot = new TelegramBot(TELEGRAM_BOT_TOKEN, { polling: true });


// listen for new messages
bot.on("message", async (msg) => {
  console.log("New message received.")
  const chatId = msg.chat.id;

  console.log("Checking for spam.")
  const { isSpam, reason } = await checkMessageForSpam(msg.text);

  if (isSpam) {
    console.log("Spam found!")
    // bot.deleteMessage(chatId, msg.message_id);
    bot.sendMessage(chatId, `This message has been marked as spam. Reason: ${reason}`);
    // store message and reason in db
    // optionally send a message to the user with the reason
  } else {
    console.log("Looks good to me.")
    bot.sendMessage(chatId, `This message looks good to me.`);
  }
})


// setup groq sdk
const groq = new Groq({ apiKey: GROQ_API_KEY });

async function checkMessageForSpam(msg: string): Promise<{
  isSpam: boolean,
  reason: string,
}> {
  const systemPrompt = `You are a chat moderator bot. You review every message to see if it's self promotion or spam. Reply to every message with a YES or NO followed by a ":" and the reason why you think it's spam or not. 
  
  Example
  - "YES: This message contains a link to a website."
  - "NO: This message is a question about the product."
  
  What we categorize as spam
  - surveys
  - link to whatsapp or telegram groups
  - job or work recruiting posts
  - looking for work posts
  - affiliate links, coupon codes, vouchers
  - messages asking people for money because people lost their money
  - non-english messages
  - etc use you understanding of spam`;

  const response = await groq.chat.completions.create({
    messages: [
      {
        role: "system",
        content: systemPrompt,
      },
      {
        role: "user",
        content: `Is the message spam? - \n${msg}`,
      },
    ],
    model: "llama-3.1-70b-versatile",
    // randomness of the generation
    temperature: 0.2,
    // maximum numer of tokens model is allowed to generate
    max_tokens: 1024,
    // likelihood-weighted options are considered. 0.5 is 50%
    top_p: 1,
    // string to stop the generation on
    stop: null,
    // whether to stream the response
    stream: false,
  });

  const { choices } = response;

  const [firstChoice] = choices;

  const [isSpamTxt, reasonTxt] = firstChoice.message.content.split(":");
  const isSpam = isSpamTxt.trim().toLowerCase() === "yes";
  const reason = reasonTxt.trim();

  return {
    isSpam,
    reason,
  };
}