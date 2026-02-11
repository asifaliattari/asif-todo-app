"""
OpenAI Client Configuration
"""

from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuration
MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
