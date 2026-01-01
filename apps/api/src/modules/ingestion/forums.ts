const BASE_URL = process.env.FORUMS_BASE_URL;
const API_KEY = process.env.FORUMS_API_KEY;


export type ForumsApiThread = {
  id: string;
  title: string;
  posts: {
    author: string;
    content: string;
  }[];
};
console.log("ENV CHECK:", {
  base: process.env.FORUMS_BASE_URL,
  key: process.env.FORUMS_API_KEY?.slice(0, 6) + "..."
});
type ForumApiResponse = {
  threads: {
    id: string;
    title: string;
    posts: {
      body: string;
      user?: { username?: string };
    }[];
  }[];
};

export async function fetchForumsThread(
  url: string
): Promise<{ success: true; data: { thread: ForumsApiThread } }> {

  const baseUrl = process.env.FORUMS_BASE_URL;
  const apiKey = process.env.FORUMS_API_KEY;

  if (!baseUrl || !apiKey) {
    throw new Error("FORUMS env vars missing");
  }

  const match = url.match(/thread\/([^/?]+)/);
  if (!match) throw new Error("Invalid thread URL");

  const slug = match[1];
console.log("🌐 Fetching from:", `${baseUrl}/api/v1/threads?query=${slug}`);

  const res = await fetch(
    `${baseUrl}/api/v1/threads?query=${encodeURIComponent(slug)}`,
    {
      headers: {
        "x-api-key": apiKey,
        "accept": "application/json"
      }
    }
  );

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Forum API error ${res.status}: ${text}`);
  }

  // ✅ FIX: explicit typing
  const json = (await res.json()) as ForumApiResponse;

  if (!json.threads || json.threads.length === 0) {
    throw new Error("Thread not found");
  }

  const thread = json.threads[0];

  return {
    success: true,
    data: {
      thread: {
        id: thread.id,
        title: thread.title,
        posts: thread.posts.map(p => ({
          author: p.user?.username ?? "unknown",
          content: p.body ?? ""
        }))
      }
    }
  };
}
