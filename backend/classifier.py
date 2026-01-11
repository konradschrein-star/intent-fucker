"""
Keyword Classifier
Handles relevance filtering and category classification using Llama 3.1
"""

from typing import Dict, List, Optional, Tuple
from ollama_client import OllamaClient
from config import (
    DEFAULT_RELEVANCE_PROMPT,
    DEFAULT_CATEGORY_PROMPT,
    DEFAULT_CONFIDENCE_THRESHOLD,
    DEFAULT_CATEGORIES
)


class KeywordClassifier:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama = ollama_client
        self.relevance_prompt_template = DEFAULT_RELEVANCE_PROMPT
        self.category_prompt_template = DEFAULT_CATEGORY_PROMPT
        self.confidence_threshold = DEFAULT_CONFIDENCE_THRESHOLD
        self.categories = DEFAULT_CATEGORIES.copy()
    
    def set_relevance_prompt(self, template: str):
        """Update the relevance filtering prompt template"""
        self.relevance_prompt_template = template
    
    def set_category_prompt(self, template: str):
        """Update the category classification prompt template"""
        self.category_prompt_template = template
    
    def set_confidence_threshold(self, threshold: int):
        """Set the confidence threshold (0-100)"""
        self.confidence_threshold = max(0, min(100, threshold))
    
    def add_category(self, category: str):
        """Add a custom category"""
        if category and category not in self.categories:
            self.categories.append(category)
    
    def remove_category(self, category: str):
        """Remove a category"""
        if category in self.categories:
            self.categories.remove(category)
    
    def get_categories(self) -> List[str]:
        """Get list of current categories"""
        return self.categories.copy()
    
    def check_relevance(self, keyword: str, topic: str) -> Tuple[bool, int, str]:
        """
        Check if a keyword is relevant to the topic
        
        Returns:
            Tuple of (is_relevant, confidence_score, reason)
        """
        # Format the prompt
        prompt = self.relevance_prompt_template.format(
            topic=topic,
            keyword=keyword
        )
        
        # Get response from Llama
        result = self.ollama.generate_json(prompt)
        
        if result:
            try:
                relevant = result.get('relevant', False)
                confidence = int(result.get('confidence', 0))
                reason = result.get('reason', 'No reason provided')
                
                # Check against threshold
                is_accepted = relevant and confidence >= self.confidence_threshold
                
                return (is_accepted, confidence, reason)
            except (ValueError, TypeError) as e:
                print(f"Error parsing relevance result: {e}")
        
        # Default to rejected if parsing fails
        return (False, 0, "Failed to analyze")
    
    def classify_category(self, keyword: str) -> Tuple[str, int, str]:
        """
        Classify keyword into a category
        
        Returns:
            Tuple of (category, confidence_score, reason)
        """
        # Format categories for prompt
        categories_str = "\n".join([f"- {cat}" for cat in self.categories])
        
        # Format the prompt
        prompt = self.category_prompt_template.format(
            keyword=keyword,
            categories=categories_str
        )
        
        # Get response from Llama
        result = self.ollama.generate_json(prompt)
        
        if result:
            try:
                category = result.get('category', 'unknown')
                confidence = int(result.get('confidence', 0))
                reason = result.get('reason', 'No reason provided')
                
                # Validate category is in our list
                if category not in self.categories:
                    category = 'unknown'
                
                return (category, confidence, reason)
            except (ValueError, TypeError) as e:
                print(f"Error parsing category result: {e}")
        
        # Default to unknown if parsing fails
        return ('unknown', 0, "Failed to classify")
    
    def classify_keyword(self, keyword: str, topic: str) -> Dict:
        """
        Perform complete classification: relevance + category
        
        Returns:
            Dictionary with all classification results
        """
        # Check relevance
        is_relevant, relevance_score, relevance_reason = self.check_relevance(keyword, topic)
        
        # Classify category
        category, category_confidence, category_reason = self.classify_category(keyword)
        
        return {
            'keyword': keyword,
            'relevance_accepted': is_relevant,
            'relevance_score': relevance_score,
            'category': category,
            'category_confidence': category_confidence,
            'reason': f"Relevance: {relevance_reason} | Category: {category_reason}"
        }


# Test function
if __name__ == "__main__":
    from ollama_client import OllamaClient
    
    client = OllamaClient()
    classifier = KeywordClassifier(client)
    
    if client.is_available():
        # Test relevance check
        result = classifier.classify_keyword(
            keyword="ys origin walkthrough",
            topic="Ys video game series"
        )
        print(f"Classification result: {result}")
    else:
        print("Ollama is not available. Please start the Ollama service.")
