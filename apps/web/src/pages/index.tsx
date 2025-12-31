import { useState, useEffect } from 'react';

interface Insight {
  text: string;
  score: number;
  type: string;
}

interface AnalysisResult {
  version: string;
  summary: string;
  sentiment: string;
  topics: string[];
  insights: Insight[];
  confidence: number;
  metadata: {
    thread_title: string;
    post_count: number;
    source: string;
    ai_provider: string;
    analyzed_at: string;
  };
}

interface ApiResponse {
  request_id: string;
  result: AnalysisResult;
  integration_status?: {
    forums_api: string;
    architecture: string;
  };
}

export default function Home() {
  const [url, setUrl] = useState('https://foru.ms/thread/ai-tools-2025');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [apiStatus, setApiStatus] = useState<'checking' | 'live' | 'demo'>('checking');

  useEffect(() => {
    checkAPIStatus();
  }, []);

  const checkAPIStatus = async () => {
    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: 'https://foru.ms/thread/test' })
      });
      const data = await res.json();
      setApiStatus(data?.integration_status?.forums_api === 'live' ? 'live' : 'demo');
    } catch {
      setApiStatus('demo');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });

      const data: ApiResponse = await res.json();

      if (!res.ok) throw new Error(data as any);

      setResult(data);
      setApiStatus(data.integration_status?.forums_api === 'live' ? 'live' : 'demo');
    } catch (err) {
      setError('Failed to analyze thread');
    } finally {
      setLoading(false);
    }
  };

  const sentimentColor = (s: string) =>
    s === 'positive' ? '#10b981' : s === 'negative' ? '#ef4444' : '#6b7280';

  return (
    <div style={{ padding: 40, maxWidth: 1200, margin: '0 auto', fontFamily: 'system-ui' }}>
      <h1>🤖 Forum Insights AI</h1>

      <form onSubmit={handleSubmit}>
        <input
          value={url}
          onChange={e => setUrl(e.target.value)}
          style={{ padding: 12, width: '70%' }}
        />
        <button disabled={loading} style={{ marginLeft: 10 }}>
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {result && (
        <>
          <h2>Analysis Result</h2>

          <p><b>Confidence:</b> {Math.round(result.result.confidence * 100)}%</p>
          <p><b>Sentiment:</b> {result.result.sentiment}</p>
          <p><b>Summary:</b> {result.result.summary}</p>

          <h3>Topics</h3>
          <ul>
            {result.result.topics.map((t, i) => (
              <li key={i}>{t}</li>
            ))}
          </ul>

          <h3>Insights</h3>
          {result.result.insights.map((i, idx) => (
            <div key={idx}>
              <b>{i.text}</b> — {Math.round(i.score * 100)}%
            </div>
          ))}

          <h3>Metadata</h3>
          <pre>{JSON.stringify(result.result.metadata, null, 2)}</pre>
        </>
      )}
    </div>
  );
}
