"""
Chat API Router
Handles AI chatbot interactions
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from anthropic import Anthropic
import os

from app.auth import get_current_user_id
import sys
from pathlib import Path
# Add backend directory to path to import mcp
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from mcp.tools import TaskTools, TOOL_DEFINITIONS


router = APIRouter(prefix="/api/chat", tags=["Chat"])


# Pydantic models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    response: str
    tool_used: Optional[str] = None
    tool_result: Optional[dict] = None


# Initialize Anthropic client
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    print("⚠️ Warning: ANTHROPIC_API_KEY not set")

client = Anthropic(api_key=anthropic_api_key) if anthropic_api_key else None


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
            detail="AI service not configured. Please set ANTHROPIC_API_KEY."
        )

    # Initialize task tools
    tools = TaskTools()

    # Build conversation history
    messages = []
    for msg in request.history[-10:]:  # Keep last 10 messages for context
        messages.append({
            "role": msg.role,
            "content": msg.content
        })

    # Add current message
    messages.append({
        "role": "user",
        "content": request.message
    })

    # System prompt
    system_prompt = """You are a helpful AI assistant for TaskFlow, a task management application.

Your job is to help users manage their tasks through natural conversation. You can:
- Create tasks when users ask
- List their tasks
- Update existing tasks
- Delete tasks
- Mark tasks as complete
- Provide statistics about their tasks

Always be friendly, helpful, and concise. When users ask about tasks, use the available tools to interact with their task list.

Examples:
- User: "Add a task to buy groceries" → Use create_task
- User: "What are my tasks?" → Use list_tasks
- User: "Mark task 123 as done" → Use mark_task_complete
- User: "Delete the meeting task" → Use delete_task (after finding task_id)

Be conversational and natural. Don't just list data - explain it in a friendly way."""

    try:
        # Call Claude API with tools
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
            tools=TOOL_DEFINITIONS
        )

        # Check if Claude wants to use a tool
        tool_used = None
        tool_result = None

        for block in response.content:
            if block.type == "tool_use":
                tool_name = block.name
                tool_input = block.input
                tool_used = tool_name

                # Execute the tool
                if tool_name == "create_task":
                    tool_result = await tools.create_task(
                        title=tool_input.get("title"),
                        description=tool_input.get("description", ""),
                        user_token=user_id  # In real impl, pass JWT token
                    )
                elif tool_name == "list_tasks":
                    tool_result = await tools.list_tasks(
                        status=tool_input.get("status", "all"),
                        user_token=user_id
                    )
                elif tool_name == "update_task":
                    tool_result = await tools.update_task(
                        task_id=tool_input.get("task_id"),
                        title=tool_input.get("title"),
                        description=tool_input.get("description"),
                        user_token=user_id
                    )
                elif tool_name == "delete_task":
                    tool_result = await tools.delete_task(
                        task_id=tool_input.get("task_id"),
                        user_token=user_id
                    )
                elif tool_name == "mark_task_complete":
                    tool_result = await tools.mark_task_complete(
                        task_id=tool_input.get("task_id"),
                        completed=tool_input.get("completed", True),
                        user_token=user_id
                    )
                elif tool_name == "get_task_stats":
                    tool_result = await tools.get_task_stats(
                        user_token=user_id
                    )

                # If tool was used, call Claude again with the result
                if tool_result:
                    messages.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": str(tool_result)
                            }
                        ]
                    })

                    # Get final response from Claude
                    final_response = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=1024,
                        system=system_prompt,
                        messages=messages
                    )

                    response_text = ""
                    for final_block in final_response.content:
                        if final_block.type == "text":
                            response_text += final_block.text

                    return ChatResponse(
                        response=response_text,
                        tool_used=tool_name,
                        tool_result=tool_result
                    )

        # No tool used, just return text response
        response_text = ""
        for block in response.content:
            if block.type == "text":
                response_text += block.text

        return ChatResponse(
            response=response_text,
            tool_used=None,
            tool_result=None
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )


@router.get("/health")
async def chat_health():
    """Check if chat service is available"""
    return {
        "status": "healthy" if client else "unavailable",
        "ai_configured": client is not None
    }
