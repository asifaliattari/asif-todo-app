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

# Anthropic API Settings
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Validate required settings
if not ANTHROPIC_API_KEY:
    print("⚠️ Warning: ANTHROPIC_API_KEY not set. AI features will not work.")
