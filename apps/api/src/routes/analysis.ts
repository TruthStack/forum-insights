import { FastifyInstance } from "fastify";
import { handleAnalysisRequest } from "../controllers/analysisController";

export default async function analysisRoutes(app: FastifyInstance) {
  app.post("/analyze", handleAnalysisRequest);
}
