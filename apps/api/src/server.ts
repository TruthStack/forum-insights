import 'dotenv/config'; // MUST be at top
const BASE_URL = process.env.FORUMS_BASE_URL;
const API_KEY = process.env.FORUMS_API_KEY;
import Fastify from "fastify";
import analysisRoutes from "./routes/analysis.js";

const app = Fastify({ logger: true });

app.register(analysisRoutes, { prefix: "/api" });

app.get("/health", async () => ({ status: "ok" }));

const PORT = Number(process.env.PORT || 4000);

app.listen({ port: PORT, host: "0.0.0.0" })
  .then(() => console.log(`🚀 API running on http://localhost:${PORT}`))
  .catch(console.error);
