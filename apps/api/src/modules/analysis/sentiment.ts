export function analyzeSentiment(text: string): 'positive' | 'neutral' | 'negative' {
  const positiveWords = ['recommend', 'helpful', 'superior', 'excels', 'best', 'great', 'love', 'excellent', 'awesome'];
  const negativeWords = ['dont', 'caution', 'over-reliance', 'avoid', 'bad', 'poor', 'terrible', 'awful'];
  
  const words = text.toLowerCase().split(/\s+/);
  
  let positiveScore = 0;
  let negativeScore = 0;
  
  words.forEach(word => {
    if (positiveWords.includes(word)) positiveScore++;
    if (negativeWords.includes(word)) negativeScore++;
  });
  
  if (positiveScore > negativeScore) return 'positive';
  if (negativeScore > positiveScore) return 'negative';
  return 'neutral';
}
