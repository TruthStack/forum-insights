import OpenAI from 'openai';


interface AIAnalysis {
  summary: string;
  sentiment: 'positive' | 'neutral' | 'negative';
  topics: string[];
  keyInsights: string[];
  confidence: number;
}

export async function summarizeWithAI(content: string): Promise<AIAnalysis> {
  try {
    const apiKey = process.env.OPENAI_API_KEY;
    
    if (!apiKey || apiKey === 'your_openai_api_key_here') {
      console.log('🎭 Using demo AI (add OpenAI API key for real analysis)');
      return getDemoAnalysis(content);
    }
    
    console.log('🤖 Using REAL OpenAI API');
    
    const openai = new OpenAI({
      apiKey: apiKey,
    });
    
    // Smart content truncation for token limits
    const truncatedContent = content.length > 12000 
      ? content.substring(0, 10000) + '\n\n[Content truncated for length...]'
      : content;
    
    const prompt = `Analyze this forum discussion thread and provide structured insights.

THREAD CONTENT:
${truncatedContent}

Please analyze and return a JSON object with this exact structure:
{
  "summary": "2-3 sentence concise summary",
  "sentiment": "positive/neutral/negative",
  "topics": ["topic1", "topic2", "topic3"],
  "keyInsights": [
    "insight 1",
    "insight 2", 
    "insight 3"
  ],
  "confidence": 0.95
}

Make the analysis practical, actionable, and focused on what matters to developers and community managers.`;
    
    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        {
          role: 'system',
          content: 'You are an expert forum analyst. You extract clear insights from community discussions.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      temperature: 0.3,
      max_tokens: 1000,
      response_format: { type: 'json_object' }
    });
    
    const result = JSON.parse(response.choices[0].message.content || '{}');
    
    // Validate and enhance result
    return {
      summary: result.summary || 'AI analysis completed successfully.',
      sentiment: (result.sentiment === 'positive' || result.sentiment === 'negative') 
        ? result.sentiment 
        : 'neutral',
      topics: Array.isArray(result.topics) ? result.topics.slice(0, 5) : ['AI', 'Development', 'Community'],
      keyInsights: Array.isArray(result.keyInsights) ? result.keyInsights.slice(0, 5) : ['Analysis complete'],
      confidence: typeof result.confidence === 'number' ? Math.min(1, Math.max(0, result.confidence)) : 0.85
    };
    
  } catch (error: any) {
    console.error('❌ OpenAI API error:', error.message);
    return getDemoAnalysis(content);
  }
}

function getDemoAnalysis(content: string): AIAnalysis {
  const isPositive = content.toLowerCase().includes('great') || content.toLowerCase().includes('recommend');
  const isNegative = content.toLowerCase().includes('problem') || content.toLowerCase().includes('issue');
  
  return {
    summary: 'This discussion explores modern AI development tools. Participants share practical experiences with different platforms and discuss implementation challenges. The conversation highlights both opportunities and considerations for teams adopting AI assistance.',
    sentiment: isPositive ? 'positive' : isNegative ? 'negative' : 'neutral',
    topics: ['AI Development', 'Tool Comparison', 'Implementation', 'Best Practices', 'Community'],
    keyInsights: [
      'Participants value practical, real-world experiences over theoretical discussions',
      'Integration complexity is a common concern across different AI platforms',
      'Community-driven knowledge sharing accelerates adoption and problem-solving',
      'Teams should consider both technical capabilities and ethical implications',
      'Hybrid approaches combining multiple AI tools yield best results'
    ],
    confidence: 0.82
  };
}
