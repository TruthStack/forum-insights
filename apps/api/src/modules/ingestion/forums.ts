export type ForumsApiThread = {
  id: string;
  title: string;
  posts: {
    author: string;
    content: string;
  }[];
};

export type ForumSuccess = {
  success: true;
  data: {
    thread: ForumsApiThread;
  };
};

export type ForumFailure = {
  success: false;
  error: string;
};

export type ForumResult = ForumSuccess | ForumFailure;

export async function fetchForumsThread(
  url: string
): Promise<ForumResult> {
  try {
    // 🔹 MOCK DATA (replace with real API later)
    const thread: ForumsApiThread = {
      id: "demo-thread",
      title: "Demo Thread",
      posts: [
        { author: "alice", content: "Great discussion!" },
        { author: "bob", content: "I learned a lot." }
      ]
    };

    return {
      success: true,
      data: { thread }
    };
  } catch (err: any) {
    return {
      success: false,
      error: err?.message ?? "Unknown error"
    };
  }
}
