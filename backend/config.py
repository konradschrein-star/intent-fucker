"""
Configuration file for the Keyword Classifier
Contains default prompts, categories, and settings
"""

# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.1:8b"

# Default Classification Settings
DEFAULT_CONFIDENCE_THRESHOLD = 75  # Percentage (0-100)

# Combined Classification Prompt Template (SINGLE CALL - FASTER!)
# Variables: {topic}, {keyword}, {categories}
DEFAULT_CLASSIFICATION_PROMPT = """You are a keyword analyzer. Analyze the keyword and determine BOTH its relevance to the topic AND its category.

Topic: {topic}
Keyword: "{keyword}"

Available Categories:
{categories}

Category Definitions:
- how-to: Step-by-step instructions to showcase or demonstrate the app/topic
- comparison: Reviews, tests, comparisons between options (e.g., "vs", "review", "best")
- walkthrough: Going over the basics or whole app without solving a specific problem (comprehensive overviews, often longer deeper videos)
- informational: General information seeking (e.g., "what is", "definition", "explained")
- transactional: Intent to take action (e.g., "download", "buy", "install")

Task:
1. Determine if the keyword is relevant to the topic (consider direct matches, synonyms, context)
2. If relevant, classify it into the most appropriate category
3. Provide confidence scores (0-100) for both decisions

Respond ONLY with a JSON object in this EXACT format (no other text):
{{"relevant": true/false, "relevance_confidence": 0-100, "category": "category-name", "category_confidence": 0-100}}

If not relevant, set category to "none" and category_confidence to 0."""

# Legacy prompts kept for backward compatibility (not used in new system)
DEFAULT_RELEVANCE_PROMPT = """You are a keyword relevance analyzer. Your task is to determine if a search keyword is relevant to a specific topic.

Topic: {topic}
Keyword: "{keyword}"

Analyze whether someone searching for this keyword is likely looking for information about the topic mentioned above. Consider:
- Direct matches and synonyms
- Context and intent
- Common variations and related terms

Respond ONLY with a JSON object in this exact format:
{{"relevant": true/false, "confidence": 0-100}}

Do not include any other text before or after the JSON."""

DEFAULT_CATEGORY_PROMPT = """You are a search intent classifier. Analyze the search keyword and classify it into one of the provided categories.

Keyword: "{keyword}"

Available Categories:
{categories}

Category Definitions:
- how-to: Step-by-step instructions to showcase or demonstrate something
- comparison: Reviews, tests, comparisons between options
- walkthrough: Comprehensive overviews without solving specific problems (longer, deeper content)
- informational: General information seeking
- transactional: Intent to take action

Respond ONLY with a JSON object in this exact format:
{{"category": "category-name", "confidence": 0-100}}

Do not include any other text before or after the JSON."""

# Default Categories
DEFAULT_CATEGORIES = [
    "how-to",
    "comparison", 
    "walkthrough",
    "informational",
    "transactional"
]

# Upload Settings
MAX_FILE_SIZE_MB = 50
ALLOWED_EXTENSIONS = {'csv'}

# CSV Column Names (expected in input)
REQUIRED_COLUMNS = ['title', 'views', 'views_per_year']

# Output CSV Column Names (removed 'reason' per user request)
OUTPUT_COLUMNS = [
    'title',
    'views', 
    'views_per_year',
    'relevance_score',
    'relevance_accepted',
    'category',
    'category_confidence'
]
