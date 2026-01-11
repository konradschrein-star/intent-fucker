"""
Keyword Classifier
Handles relevance filtering and category classification using Llama 3.1
OPTIMIZED: Now uses SINGLE AI call instead of TWO (2x faster!)
"""

from typing import Dict, List, Optional, Tuple
from ollama_client import OllamaClient
from config import (
    DEFAULT_CLASSIFICATION_PROMPT,
    DEFAULT_RELEVANCE_PROMPT,
    DEFAULT_CATEGORY_PROMPT,
    DEFAULT_CONFIDENCE_THRESHOLD,
    DEFAULT_CATEGORIES
)


class KeywordClassifier:
    """
    This is the brain of the app! It uses AI to classify keywords.
    
    OPTIMIZED APPROACH:
    - Uses ONE AI call instead of TWO (2x faster processing!)
    - Removes unnecessary "reason" field (faster responses)
    - Combined relevance + category classification
    
    For each keyword, it determines:
    1. RELEVANCE: "Is this keyword actually about the topic?"
       Example: If topic is "Ys games", "ys origin" = relevant, "yes button" = not relevant
       
    2. CATEGORY: "What type of search is this?"
       Example: "how to install" = how-to, "ys vs trails" = comparison
    
    Think of it like a smart filter that:
    - Throws out irrelevant keywords (the junk)
    - Labels the good keywords by what users are looking for
    """
    
    def __init__(self, ollama_client: OllamaClient):
        # The AI client we use to talk to Llama 3.1
        self.ollama = ollama_client
        
        # The COMBINED prompt template (does both relevance + category in ONE call!)
        self.classification_prompt_template = DEFAULT_CLASSIFICATION_PROMPT
        
        # Legacy prompts (kept for backward compatibility if user customized them)
        self.relevance_prompt_template = DEFAULT_RELEVANCE_PROMPT
        self.category_prompt_template = DEFAULT_CATEGORY_PROMPT
        
        # Minimum confidence score to accept a keyword (0-100)
        # Example: 75 means "at least 75% sure it's relevant"
        self.confidence_threshold = DEFAULT_CONFIDENCE_THRESHOLD
        
        # List of categories available (how-to, comparison, etc.)
        self.categories = DEFAULT_CATEGORIES.copy()
    
    def set_relevance_prompt(self, template: str):
        """Update the relevance filtering prompt template (legacy support)"""
        self.relevance_prompt_template = template
    
    def set_category_prompt(self, template: str):
        """Update the category classification prompt template (legacy support)"""
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
    
    def get_categories() -> List[str]:
        """Get list of current categories"""
        return self.categories.copy()
    
    def classify_keyword_combined(self, keyword: str, topic: str) -> Dict:
        """
        OPTIMIZED: Perform BOTH relevance and category classification in ONE AI call!
        
        This is 2x faster than the old approach (which made 2 separate calls).
        
        Args:
            keyword: The search term to analyze
            topic: What the keyword should be about
            
        Returns:
            Dictionary with all classification results:
            - relevance_accepted: True/False
            - relevance_score: 0-100
            - category: category name
            - category_confidence: 0-100
        """
        # Format categories for prompt
        categories_str = "\n".join([f"- {cat}" for cat in self.categories])
        
        # Format the COMBINED prompt
        prompt = self.classification_prompt_template.format(
            topic=topic,
            keyword=keyword,
            categories=categories_str
        )
        
        # Get response from Llama (ONE call does everything!)
        result = self.ollama.generate_json(prompt)
        
        if result:
            try:
                # Parse the response
                relevant = result.get('relevant', False)
                relevance_confidence = int(result.get('relevance_confidence', 0))
                category = result.get('category', 'unknown')
                category_confidence = int(result.get('category_confidence', 0))
                
                # Validate category
                if category not in self.categories and category != 'none':
                    category = 'unknown'
                
                # Check against threshold
                is_accepted = relevant and relevance_confidence >= self.confidence_threshold
                
                return {
                    'keyword': keyword,
                    'relevance_accepted': is_accepted,
                    'relevance_score': relevance_confidence,
                    'category': category if is_accepted else 'none',
                    'category_confidence': category_confidence if is_accepted else 0
                }
            except (ValueError, TypeError) as e:
                print(f"Error parsing combined classification result: {e}")
        
        # Default to rejected if parsing fails
        return {
            'keyword': keyword,
            'relevance_accepted': False,
            'relevance_score': 0,
            'category': 'none',
            'category_confidence': 0
        }
    
    def check_relevance(self, keyword: str, topic: str) -> Tuple[bool, int]:
        """
        Legacy method: Check only relevance (SLOWER - use classify_keyword_combined instead!)
        Kept for backward compatibility.
        """
        prompt = self.relevance_prompt_template.format(
            topic=topic,
            keyword=keyword
        )
        
        result = self.ollama.generate_json(prompt)
        
        if result:
            try:
                relevant = result.get('relevant', False)
                confidence = int(result.get('confidence', 0))
                is_accepted = relevant and confidence >= self.confidence_threshold
                return (is_accepted, confidence)
            except (ValueError, TypeError) as e:
                print(f"Error parsing relevance result: {e}")
        
        return (False, 0)
    
    def classify_category(self, keyword: str) -> Tuple[str, int]:
        """
        Legacy method: Classify only category (SLOWER - use classify_keyword_combined instead!)
        Kept for backward compatibility.
        """
        categories_str = "\n".join([f"- {cat}" for cat in self.categories])
        
        prompt = self.category_prompt_template.format(
            keyword=keyword,
            categories=categories_str
        )
        
        result = self.ollama.generate_json(prompt)
        
        if result:
            try:
                category = result.get('category', 'unknown')
                confidence = int(result.get('confidence', 0))
                
                if category not in self.categories:
                    category = 'unknown'
                
                return (category, confidence)
            except (ValueError, TypeError) as e:
                print(f"Error parsing category result: {e}")
        
        return ('unknown', 0)
    
    def classify_keyword(self, keyword: str, topic: str) -> Dict:
        """
        Main classification method - uses OPTIMIZED single-call approach!
        
        This is the method called by the backend during processing.
        """
        return self.classify_keyword_combined(keyword, topic)


# Test function
if __name__ == "__main__":
    from ollama_client import OllamaClient
    
    client = OllamaClient()
    classifier = KeywordClassifier(client)
    
    if client.is_available():
        # Test combined classification
        result = classifier.classify_keyword(
            keyword="ys origin walkthrough",
            topic="Ys video game series"
        )
        print(f"Combined classification result: {result}")
    else:
        print("Ollama is not available. Please start the Ollama service.")
