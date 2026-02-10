"""
MCP Server Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

# MCP Server Settings
MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "localhost")
MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", "5000"))

# Backend API Settings
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

# OpenAI API Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # or gpt-4, gpt-3.5-turbo

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Validate required settings
if not OPENAI_API_KEY:
    print("⚠️ Warning: OPENAI_API_KEY not set. AI features will not work.")
