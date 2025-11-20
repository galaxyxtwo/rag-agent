import os
from dotenv import load_dotenv
load_dotenv()

# Configuration settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DOCUMENT_PATH = os.path.join(BASE_DIR, "docs", "issues.md")
VECTOR_STORE_DIR = "./chroma_db"
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# API Configuration - can be overridden by .env file
API_URL = os.getenv("API_URL", "http://localhost:3000/v1/chat/completions")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "Qwen3-0.6B")
DEFAULT_MAX_TOKENS = int(os.getenv("DEFAULT_MAX_TOKENS", "1024"))
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.0"))

# Get API token from environment or set None
DEFAULT_API_TOKEN = os.getenv("API_TOKEN")