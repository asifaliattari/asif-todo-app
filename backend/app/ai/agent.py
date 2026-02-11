"""
OpenAI Agent Execution Logic
Main agent that processes messages and executes MCP tools
"""

from openai import AsyncOpenAI, OpenAIError
from mcp.tools import TaskTools
from .tools import get_openai_tools
from .prompts import SYSTEM_PROMPT
from .openai_client import client, MODEL, MAX_TOKENS, TEMPERATURE
import json
from typing import Tuple, List, Dict, Any
import os
from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime objects"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


async def run_agent(
    messages: List[Dict[str, str]],
    user_id: str,
    user_token: str
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Run OpenAI agent with MCP tools

    Args:
        messages: Conversation history (list of {"role": "user/assistant", "content": "..."})
        user_id: User ID for tool execution
        user_token: JWT token for backend API calls

    Returns:
        Tuple of (response_text, tool_calls_list)
    """

    # Initialize MCP tools handler
    backend_url = os.getenv("BACKEND_API_URL", "http://localhost:8000")
    tools_handler = TaskTools(backend_url=backend_url)

    # Get OpenAI-formatted tools
    tools = get_openai_tools()

    # Add system message
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    try:
        # Call OpenAI API
        response = await client.chat.completions.create(
            model=MODEL,
            messages=full_messages,
            tools=tools,
            tool_choice="auto",  # Let model decide when to call tools
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

        assistant_message = response.choices[0].message
        tool_calls = assistant_message.tool_calls or []

        # Execute tool calls if any
        tool_results = []
        if tool_calls:
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                try:
                    tool_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    tool_args = {}

                # Add user token for authentication
                tool_args["user_token"] = user_token

                # Execute tool via MCP
                result = await execute_mcp_tool(tools_handler, tool_name, tool_args)

                tool_results.append({
                    "tool": tool_name,
                    "parameters": {k: v for k, v in tool_args.items() if k != "user_token"},  # Don't store token
                    "result": result
                })

            # If tools were called, make a second API call to get final response
            # Add tool calls to conversation
            tool_calls_for_api = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in tool_calls
            ]

            full_messages.append({
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": tool_calls_for_api
            })

            # Add tool results
            for i, tool_call in enumerate(tool_calls):
                full_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_results[i]["result"], cls=DateTimeEncoder)
                })

            # Get final response
            final_response = await client.chat.completions.create(
                model=MODEL,
                messages=full_messages,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            )

            response_text = final_response.choices[0].message.content or "Done!"
        else:
            # No tools called, just return the response
            response_text = assistant_message.content or "I'm not sure how to help with that."
            tool_results = []

        return response_text, tool_results

    except OpenAIError as e:
        print(f"OpenAI API Error: {str(e)}")
        return f"I encountered an error: {str(e)}", []
    except Exception as e:
        print(f"Agent Error: {str(e)}")
        return "I'm having trouble processing your request. Please try again.", []


async def execute_mcp_tool(
    tools_handler: TaskTools,
    tool_name: str,
    args: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute MCP tool and return result

    Args:
        tools_handler: TaskTools instance
        tool_name: Name of the tool to execute
        args: Tool arguments including user_token

    Returns:
        Tool execution result
    """
    try:
        if tool_name == "create_task":
            return await tools_handler.create_task(**args)
        elif tool_name == "list_tasks":
            return await tools_handler.list_tasks(**args)
        elif tool_name == "update_task":
            return await tools_handler.update_task(**args)
        elif tool_name == "delete_task":
            return await tools_handler.delete_task(**args)
        elif tool_name == "mark_task_complete":
            return await tools_handler.mark_task_complete(**args)
        elif tool_name == "get_task_stats":
            return await tools_handler.get_task_stats(**args)
        else:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}",
                "error_code": "UNKNOWN_TOOL"
            }
    except Exception as e:
        print(f"Tool Execution Error ({tool_name}): {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "error_code": "TOOL_EXECUTION_ERROR"
        }
