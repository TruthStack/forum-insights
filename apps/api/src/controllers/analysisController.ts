import { FastifyRequest, FastifyReply } from "fastify";
import { orchestrateAnalysis } from "../orchestrator";

export async function handleAnalysisRequest(
  request: FastifyRequest,
  reply: FastifyReply
) {
  try {
    const body = request.body as any;

    if (!body || typeof body.url !== "string") {
      return reply.status(400).send({
        error_code: "INVALID_REQUEST",
        message: "Missing or invalid \"url\" field"
      });
    }

    const requestId = crypto.randomUUID();

    // Call orchestrator
    const result = await orchestrateAnalysis({
      request_id: requestId,
      url: body.url
    });

    return reply.status(200).send({
      request_id: requestId,
      accepted: true,
      result: result.result
    });
  } catch (err) {
    return reply.status(500).send({
      error_code: "INTERNAL_ERROR",
      message: "Unexpected server error"
    });
  }
}
