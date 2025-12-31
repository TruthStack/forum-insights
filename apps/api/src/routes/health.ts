import { FastifyInstance } from "fastify";

export default async function healthRoutes(app: FastifyInstance) {
  app.get('/health', async (request, reply) => {
    return {
      status: 'ok',
      service: 'forum-insights-api',
      version: '1.0.0',
      timestamp: new Date().toISOString(),
      hackathon: 'Foru.ms x Vercel',
      ready: true
    };
  });
}
