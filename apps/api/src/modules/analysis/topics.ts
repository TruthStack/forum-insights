export function extractTopics(text: string): string[] {
  const commonTopics = [
    'AI', 'coding', 'development', 'tools', 'assistants',
    'learning', 'best practices', 'productivity', 'programming',
    'beginners', 'senior developers', 'GitHub', 'Claude', 'GPT-4'
  ];
  
  const foundTopics: string[] = [];
  const lowerText = text.toLowerCase();
  
  commonTopics.forEach(topic => {
    if (lowerText.includes(topic.toLowerCase())) {
      foundTopics.push(topic);
    }
  });
  
  // Add some smart extraction
  if (lowerText.includes('junior') || lowerText.includes('beginner')) {
    foundTopics.push('beginner friendly');
  }
  
  if (lowerText.includes('senior') || lowerText.includes('experienced')) {
    foundTopics.push('expert advice');
  }
  
  // Remove duplicates and limit
  return [...new Set(foundTopics)].slice(0, 5);
}
