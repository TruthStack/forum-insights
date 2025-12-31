#!/bin/bash

echo "🚀 Starting Forum Insights AI - Foru.ms x Vercel Hackathon"
echo "=========================================================="
echo ""

# Check for API keys
if [ -f "apps/api/.env" ]; then
  if grep -q "your_openai_api_key_here" apps/api/.env; then
    echo "⚠️  WARNING: OpenAI API key not set"
    echo "   Get one from: https://platform.openai.com/api-keys"
  else
    echo "✅ OpenAI API key configured"
  fi
  
  if grep -q "your_forums_api_key_here" apps/api/.env; then
    echo "⚠️  WARNING: Foru.ms API key not set"
    echo "   Get one from: https://foru.ms/developers"
  else
    echo "✅ Foru.ms API key configured"
  fi
else
  echo "❌ No .env file found. Creating template..."
  cp apps/api/.env.example apps/api/.env 2>/dev/null || echo "Please create apps/api/.env"
fi

echo ""
echo "📡 Starting servers..."
echo ""

# Start API server
echo "🌐 API Server (Port 4000)..."
cd apps/api
npm run dev &
API_PID=$!
cd ../..

# Wait a moment for API to start
sleep 2

# Start Web server
echo "🖥️  Web Server (Port 3000)..."
cd apps/web
npm run dev &
WEB_PID=$!
cd ../..

echo ""
echo "✅ Servers starting..."
echo ""
echo "🌐 API:  http://localhost:4000"
echo "     Health: http://localhost:4000/health"
echo "     Test:   curl -X POST http://localhost:4000/api/analyze \\"
echo '               -H "Content-Type: application/json" \\'
echo '               -d \'{"url":"https://foru.ms/thread/sample"}\''
echo ""
echo "🖥️  Web UI: http://localhost:3000"
echo ""
echo "📋 Press Ctrl+C to stop both servers"
echo ""

# Trap Ctrl+C to clean up
trap "echo ''; echo '🛑 Stopping servers...'; kill $API_PID $WEB_PID 2>/dev/null; exit 0" INT

# Wait for both processes
wait $API_PID $WEB_PID
