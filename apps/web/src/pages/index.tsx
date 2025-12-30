import { useState } from 'react';

export default function Home() {
  const [url, setUrl] = useState('https://foru.ms/thread/demo');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setResult(data);
      } else {
        setError(data.message || 'Analysis failed');
      }
    } catch (error) {
      setError('Network error - Make sure API server is running on port 3000');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 40, fontFamily: 'sans-serif' }}>
      <h1>🤖 Forum Insights AI</h1>
      <p>Paste a forum thread URL to get AI-powered insights (Hackathon Demo)</p>
      
      <form onSubmit={handleSubmit} style={{ marginTop: 20 }}>
        <input 
          type="url" 
          placeholder="https://foru.ms/thread/123"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{ padding: 10, width: 400, fontSize: 16 }}
          required
        />
        <button 
          type="submit"
          style={{ 
            padding: '10px 20px', 
            marginLeft: 10,
            fontSize: 16,
            background: loading ? '#ccc' : '#0070f3',
            color: 'white',
            border: 'none',
            borderRadius: 5,
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
          disabled={loading}
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </form>
      
      {error && (
        <div style={{ 
          background: '#ffebee', 
          padding: 15, 
          borderRadius: 6,
          marginTop: 20,
          color: '#c62828'
        }}>
          <strong>Error:</strong> {error}
        </div>
      )}
      
      {result && (
        <div style={{ marginTop: 40 }}>
          <h2>Results</h2>
          <div style={{ background: '#f5f5f5', padding: 20, borderRadius: 8 }}>
            <h3>Summary:</h3>
            <pre style={{ 
              background: 'white', 
              padding: 15, 
              borderRadius: 5,
              overflow: 'auto',
              whiteSpace: 'pre-wrap'
            }}>
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        </div>
      )}
      
      <div style={{ marginTop: 40, color: '#666' }}>
        <h3>Foru.ms x Vercel Hackathon Demo</h3>
        <ul>
          <li>✅ Modular architecture implemented</li>
          <li>✅ API Gateway with validation</li>
          <li>✅ Mock AI analysis working</li>
          <li>✅ Ready for real Foru.ms API integration</li>
          <li>✅ Ready for real OpenAI integration</li>
        </ul>
      </div>
    </div>
  );
}
