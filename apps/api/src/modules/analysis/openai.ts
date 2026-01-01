import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY!,
});

export async function analyzeThreadWithAI(text: string) {
  const completion = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: "Summarize forum threads and extract insights."
      },
      {
        role: "user",
        content: text
      }
    ],
    temperature: 0.3
  });

  return completion.choices[0].message.content;
}
