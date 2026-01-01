import { FastifyRequest, FastifyReply } from "fastify";
import { orchestrateAnalysis } from "../orchestrator";
const BASE_URL = process.env.FORUMS_BASE_URL;
const API_KEY = process.env.FORUMS_API_KEY;
type AnalyzeRequestBody = {
  url: string;
};

export async function handleAnalysisRequest(
  request: FastifyRequest<{ Body: AnalyzeRequestBody }>,
  reply: FastifyReply
) {
  try {
    const { url } = request.body;

    if (!url || typeof url !== "string") {
      return reply.status(400).send({
        error: "Invalid or missing URL"
      });
    }

    console.log("📨 Processing request for:", url);

    const result = await orchestrateAnalysis({
      request_id: `req_${Date.now()}`,
      url
    });

    return reply.status(200).send(result);
  } catch (error: any) {
    console.error("❌ Controller error:", error);

    return reply.status(500).send({
      error: "Analysis service temporarily unavailable",
      message: error?.message ?? "Unknown error"
    });
  }
}
