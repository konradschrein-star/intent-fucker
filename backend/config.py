"""
Configuration file for the Keyword Classifier
Contains default prompts, categories, and settings
"""

# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.1:8b"

# Default Classification Settings
DEFAULT_CONFIDENCE_THRESHOLD = 75  # Percentage (0-100)

# Default Relevance Filter Prompt Template
# Variables: {topic}, {keyword}
DEFAULT_RELEVANCE_PROMPT = """You are a keyword relevance analyzer. Your task is to determine if a search keyword is relevant to a specific topic.

Topic: {topic}
Keyword: "{keyword}"

Analyze whether someone searching for this keyword is likely looking for information about the topic mentioned above. Consider:
- Direct matches and synonyms
- Context and intent
- Common variations and related terms

Respond ONLY with a JSON object in this exact format:
{{"relevant": true/false, "confidence": 0-100, "reason": "brief explanation"}}

Do not include any other text before or after the JSON."""

# Default Category Classification Prompt Template
# Variables: {keyword}, {categories}
DEFAULT_CATEGORY_PROMPT = """You are a search intent classifier. Analyze the search keyword and classify it into one of the provided categories.

Keyword: "{keyword}"

Available Categories:
{categories}

Category Definitions:
- how-to: User wants to learn how to do something (e.g., "how to install", "tutorial")
- comparison: User is comparing options (e.g., "vs", "best", "comparison")
- walkthrough: User wants step-by-step guidance (e.g., "guide", "walkthrough", "step by step")
- informational: User seeks general information (e.g., "what is", "definition", "meaning")
- transactional: User intends to take action/purchase (e.g., "download", "buy", "price")

Respond ONLY with a JSON object in this exact format:
{{"category": "category-name", "confidence": 0-100, "reason": "brief explanation"}}

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

# Output CSV Column Names
OUTPUT_COLUMNS = [
    'title',
    'views', 
    'views_per_year',
    'relevance_score',
    'relevance_accepted',
    'category',
    'category_confidence',
    'reason'
]
