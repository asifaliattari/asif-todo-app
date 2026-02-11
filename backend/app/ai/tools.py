"""
Tool Definitions Converter
Converts MCP tool definitions to OpenAI function calling format
"""

from mcp.tools import TOOL_DEFINITIONS


def get_openai_tools() -> list[dict]:
    """
    Convert MCP tool definitions to OpenAI function calling format

    Returns:
        List of OpenAI tool definitions
    """
    openai_tools = []

    for mcp_tool in TOOL_DEFINITIONS:
        openai_tool = {
            "type": "function",
            "function": {
                "name": mcp_tool["name"],
                "description": mcp_tool["description"],
                "parameters": mcp_tool["input_schema"]
            }
        }
        openai_tools.append(openai_tool)

    return openai_tools
