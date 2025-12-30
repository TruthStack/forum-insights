import Fastify from "fastify";
import analysisRoutes from "./routes/analysis";

const app = Fastify({ logger: true });

app.register(analysisRoutes, { prefix: "/api" });

// Add root route for health check
app.get("/", async (request, reply) => {
  return { status: "ok", message: "Forum Insights API" };
});

const start = async () => {
  try {
    const port = process.env.PORT ? parseInt(process.env.PORT) : 3000;
    await app.listen({ port, host: "0.0.0.0" });
    console.log(`API Gateway running on http://localhost:${port}`);
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
};

start();
