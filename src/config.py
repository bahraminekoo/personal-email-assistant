import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
ASSISTANT_NAME = os.getenv("EMAIL_ASSISTANT_NAME", "Personal Email Assistant")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "Qwen3-0.6B") # flan-t5-small

if not HF_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY not set. Create a .env file or set environment variable.")
