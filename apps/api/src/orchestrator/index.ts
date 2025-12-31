import { fetchForumsThread } from "../modules/ingestion/forums";

type OrchestrateInput = {
  request_id: string;
  url: string;
};

type OrchestrateResponse = {
  request_id: string;
  result: {
    version: string;
    summary: string;
    sentiment: string;
    topics: string[];
    insights: {
      text: string;
      score: number;
      type: string;
    }[];
    confidence: number;
    metadata: {
      thread_title: string;
      thread_id: string;
      post_count: number;
      unique_authors: number;
      analyzed_at: string;
    };
  };
};

export async function orchestrateAnalysis(
  input: OrchestrateInput
): Promise<OrchestrateResponse> {

  console.log("🚀 Starting analysis:", input.url);

  const forumResult = await fetchForumsThread(input.url);

  // ✅ SAFE DISCRIMINATED UNION CHECK
  if (!forumResult.success) {
    throw new Error(forumResult.error);
  }

  const thread = forumResult.data.thread;
  const uniqueAuthors = new Set(thread.posts.map(p => p.author));

  return {
    request_id: input.request_id,
    result: {
      version: "v1",
      summary: `Thread contains ${thread.posts.length} posts`,
      sentiment: "neutral",
      topics: ["discussion", "community"],
      insights: [
        {
          text: `Total posts: ${thread.posts.length}`,
          score: 0.9,
          type: "activity"
        },
        {
          text: `Unique authors: ${uniqueAuthors.size}`,
          score: 0.85,
          type: "engagement"
        }
      ],
      confidence: 0.9,
      metadata: {
        thread_title: thread.title,
        thread_id: thread.id,
        post_count: thread.posts.length,
        unique_authors: uniqueAuthors.size,
        analyzed_at: new Date().toISOString()
      }
    }
  };
}
