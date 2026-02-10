"""
Chat API Router - Direct Database Access
Handles AI chatbot interactions with OpenAI using direct database access
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List
from openai import OpenAI
from sqlmodel import Session, select
from datetime import datetime
import os
import json

from app.auth import get_current_user_id, security
from app.database import get_session
from app.models.task import Task, TaskCreate, TaskResponse

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
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Send a message to the AI chatbot with direct database access

    The AI can use tools to manage tasks on behalf of the user.
    """
    if not client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service not configured. Please set OPENAI_API_KEY."
        )

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

                # Execute the tool with direct database access
                tool_result = None

                try:
                    if function_name == "create_task":
                        # Create task directly in database
                        title = function_args.get("title", "").strip()
                        description = function_args.get("description", "").strip()

                        task = Task(
                            user_id=user_id,
                            title=title,
                            description=description if description else None,
                            completed=False
                        )
                        session.add(task)
                        session.commit()
                        session.refresh(task)

                        tool_result = {
                            "success": True,
                            "task": TaskResponse.model_validate(task).model_dump(),
                            "message": f"Created task: {title}"
                        }

                    elif function_name == "list_tasks":
                        # List tasks from database
                        status_filter = function_args.get("status", "all")
                        statement = select(Task).where(Task.user_id == user_id)

                        if status_filter == "active":
                            statement = statement.where(Task.completed == False)
                        elif status_filter == "completed":
                            statement = statement.where(Task.completed == True)

                        statement = statement.order_by(Task.created_at.desc())
                        tasks = session.exec(statement).all()

                        tool_result = {
                            "success": True,
                            "tasks": [TaskResponse.model_validate(t).model_dump() for t in tasks],
                            "count": len(tasks)
                        }

                    elif function_name == "update_task":
                        # Update task in database
                        task_id = int(function_args.get("task_id"))
                        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
                        task = session.exec(statement).first()

                        if task:
                            if "title" in function_args and function_args["title"]:
                                task.title = function_args["title"].strip()
                            if "description" in function_args:
                                task.description = function_args["description"].strip() if function_args["description"] else None
                            if "completed" in function_args:
                                task.completed = function_args["completed"]

                            task.updated_at = datetime.utcnow()
                            session.add(task)
                            session.commit()
                            session.refresh(task)

                            tool_result = {
                                "success": True,
                                "task": TaskResponse.model_validate(task).model_dump(),
                                "message": "Task updated successfully"
                            }
                        else:
                            tool_result = {
                                "success": False,
                                "task": None,
                                "message": "Task not found"
                            }

                    elif function_name == "delete_task":
                        # Delete task from database
                        task_id = int(function_args.get("task_id"))
                        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
                        task = session.exec(statement).first()

                        if task:
                            session.delete(task)
                            session.commit()
                            tool_result = {
                                "success": True,
                                "message": "Task deleted successfully"
                            }
                        else:
                            tool_result = {
                                "success": False,
                                "message": "Task not found"
                            }

                    elif function_name == "mark_task_complete":
                        # Mark task complete in database
                        task_id = int(function_args.get("task_id"))
                        completed = function_args.get("completed", True)
                        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
                        task = session.exec(statement).first()

                        if task:
                            task.completed = completed
                            task.updated_at = datetime.utcnow()
                            session.add(task)
                            session.commit()
                            session.refresh(task)

                            tool_result = {
                                "success": True,
                                "task": TaskResponse.model_validate(task).model_dump(),
                                "message": f"Task marked as {'complete' if completed else 'incomplete'}"
                            }
                        else:
                            tool_result = {
                                "success": False,
                                "task": None,
                                "message": "Task not found"
                            }

                    elif function_name == "get_task_stats":
                        # Get task statistics from database
                        statement = select(Task).where(Task.user_id == user_id)
                        tasks = session.exec(statement).all()

                        total = len(tasks)
                        completed = sum(1 for t in tasks if t.completed)
                        active = total - completed
                        completion_rate = round((completed / total * 100) if total > 0 else 0, 1)

                        tool_result = {
                            "success": True,
                            "stats": {
                                "total": total,
                                "active": active,
                                "completed": completed,
                                "completion_rate": completion_rate
                            }
                        }

                except Exception as e:
                    print(f"Tool execution error: {str(e)}")
                    tool_result = {
                        "success": False,
                        "message": f"Error: {str(e)}"
                    }

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
