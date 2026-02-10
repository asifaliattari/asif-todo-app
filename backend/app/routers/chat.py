"""
Chat API Router
Handles AI chatbot interactions with OpenAI
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from openai import OpenAI
import os
import json

from app.auth import get_current_user_id
import sys
from pathlib import Path
# Add backend directory to path to import mcp
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from mcp.tools import TaskTools


router = APIRouter(prefix="/api/chat", tags=["Chat"])


# Pydantic models
class ChatMessage(BaseModel):
    role: str  # "user", "assistant", or "system"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    response: str
    tool_used: Optional[str] = None
    tool_result: Optional[dict] = None


# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not openai_api_key:
    print("⚠️ Warning: OPENAI_API_KEY not set")

client = OpenAI(api_key=openai_api_key) if openai_api_key else None


# Define tools in OpenAI function calling format
OPENAI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Create a new task. Use this when the user wants to add a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of the task"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List the user's tasks. Use this when the user asks about their tasks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "active", "completed"],
                        "description": "Filter tasks by status (default: all)"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update an existing task. Use this when the user wants to modify a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description for the task"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task. Use this when the user wants to remove a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mark_task_complete",
            "description": "Mark a task as complete or incomplete. Use when user says they finished a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task"
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "True to mark complete, False to mark incomplete"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_task_stats",
            "description": "Get statistics about the user's tasks. Use when user asks about their progress.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Send a message to the AI chatbot

    The AI can use tools to manage tasks on behalf of the user.
    """
    if not client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service not configured. Please set OPENAI_API_KEY."
        )

    # Initialize task tools
    tools = TaskTools()

    # Build conversation history
    messages = [
        {
            "role": "system",
            "content": """You are a helpful and friendly AI assistant for TaskFlow, a task management application.

Your personality:
- Warm, enthusiastic, and encouraging
- Use a conversational, human-like tone
- Be concise but helpful
- Use emojis occasionally to add warmth
- Celebrate user accomplishments

Your job is to help users manage their tasks through natural conversation. You can:
- Create tasks when users ask
- List their tasks
- Update existing tasks
- Delete tasks
- Mark tasks as complete
- Provide statistics about their tasks

Always be encouraging and make task management feel easy and rewarding!

Examples:
- User: "Add a task to buy groceries" → Use create_task, then say something like "Got it! I've added 'Buy groceries' to your list 🛒"
- User: "What are my tasks?" → Use list_tasks, then present them in a friendly way
- User: "I finished the first task!" → Use mark_task_complete, celebrate their progress
- User: "Delete the meeting task" → First use list_tasks to find it, then delete_task

Remember: Be conversational and encouraging. Make task management feel like chatting with a helpful friend!"""
        }
    ]

    # Add history (keep last 10 messages for context)
    for msg in request.history[-10:]:
        messages.append({
            "role": msg.role,
            "content": msg.content
        })

    # Add current message
    messages.append({
        "role": "user",
        "content": request.message
    })

    try:
        # Call OpenAI API with function calling
        response = client.chat.completions.create(
            model=openai_model,
            messages=messages,
            tools=OPENAI_TOOLS,
            tool_choice="auto"  # Let AI decide when to use tools
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # Check if AI wants to use a tool
        if tool_calls:
            # Add assistant's response to messages
            messages.append(response_message)

            # Execute each tool call
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Execute the tool
                tool_result = None
                if function_name == "create_task":
                    tool_result = await tools.create_task(
                        title=function_args.get("title"),
                        description=function_args.get("description", ""),
                        user_token=user_id
                    )
                elif function_name == "list_tasks":
                    tool_result = await tools.list_tasks(
                        status=function_args.get("status", "all"),
                        user_token=user_id
                    )
                elif function_name == "update_task":
                    tool_result = await tools.update_task(
                        task_id=function_args.get("task_id"),
                        title=function_args.get("title"),
                        description=function_args.get("description"),
                        user_token=user_id
                    )
                elif function_name == "delete_task":
                    tool_result = await tools.delete_task(
                        task_id=function_args.get("task_id"),
                        user_token=user_id
                    )
                elif function_name == "mark_task_complete":
                    tool_result = await tools.mark_task_complete(
                        task_id=function_args.get("task_id"),
                        completed=function_args.get("completed", True),
                        user_token=user_id
                    )
                elif function_name == "get_task_stats":
                    tool_result = await tools.get_task_stats(
                        user_token=user_id
                    )

                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(tool_result)
                })

            # Get final response from GPT with tool results
            final_response = client.chat.completions.create(
                model=openai_model,
                messages=messages
            )

            final_message = final_response.choices[0].message.content

            return ChatResponse(
                response=final_message,
                tool_used=tool_calls[0].function.name if tool_calls else None,
                tool_result=tool_result
            )

        # No tool used, just return text response
        return ChatResponse(
            response=response_message.content,
            tool_used=None,
            tool_result=None
        )

    except Exception as e:
        print(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )


@router.get("/health")
async def chat_health():
    """Check if chat service is available"""
    return {
        "status": "healthy" if client else "unavailable",
        "ai_configured": client is not None,
        "model": openai_model if client else None
    }
