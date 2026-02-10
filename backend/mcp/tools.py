"""
MCP Tools for Task Management
Defines tools that Claude AI can use to manage tasks
"""
from typing import Any, Dict, Optional
import httpx
from .config import BACKEND_API_URL


class TaskTools:
    """Task management tools for MCP"""

    def __init__(self, backend_url: str = BACKEND_API_URL):
        self.backend_url = backend_url

    async def _call_api(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict] = None,
        user_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Call backend API with authentication"""
        headers = {}
        if user_token:
            headers["Authorization"] = f"Bearer {user_token}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=f"{self.backend_url}{endpoint}",
                    json=data,
                    headers=headers,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                return {
                    "success": False,
                    "error": str(e),
                    "error_code": "API_ERROR"
                }

    async def create_task(
        self,
        title: str,
        description: str = "",
        user_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new task

        Args:
            title: Task title (required)
            description: Task description (optional)
            user_token: User JWT token for authentication

        Returns:
            Dictionary with success status and task data
        """
        data = {
            "title": title,
            "description": description,
            "completed": False
        }

        result = await self._call_api(
            endpoint="/api/tasks",
            method="POST",
            data=data,
            user_token=user_token
        )

        return {
            "success": True if "id" in result else False,
            "task": result if "id" in result else None,
            "message": f"Created task: {title}" if "id" in result else "Failed to create task"
        }

    async def list_tasks(
        self,
        status: str = "all",
        user_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List user's tasks

        Args:
            status: Filter by status (all, active, completed)
            user_token: User JWT token for authentication

        Returns:
            Dictionary with success status and list of tasks
        """
        result = await self._call_api(
            endpoint="/api/tasks",
            method="GET",
            user_token=user_token
        )

        if isinstance(result, list):
            tasks = result

            # Filter by status if specified
            if status == "active":
                tasks = [t for t in tasks if not t.get("completed", False)]
            elif status == "completed":
                tasks = [t for t in tasks if t.get("completed", False)]

            return {
                "success": True,
                "tasks": tasks,
                "count": len(tasks)
            }

        return {
            "success": False,
            "tasks": [],
            "count": 0,
            "error": result.get("error", "Failed to fetch tasks")
        }

    async def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
        user_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update an existing task

        Args:
            task_id: ID of task to update
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)
            user_token: User JWT token for authentication

        Returns:
            Dictionary with success status and updated task
        """
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if completed is not None:
            data["completed"] = completed

        result = await self._call_api(
            endpoint=f"/api/tasks/{task_id}",
            method="PUT",
            data=data,
            user_token=user_token
        )

        return {
            "success": True if "id" in result else False,
            "task": result if "id" in result else None,
            "message": "Task updated successfully" if "id" in result else "Failed to update task"
        }

    async def delete_task(
        self,
        task_id: str,
        user_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Delete a task

        Args:
            task_id: ID of task to delete
            user_token: User JWT token for authentication

        Returns:
            Dictionary with success status
        """
        result = await self._call_api(
            endpoint=f"/api/tasks/{task_id}",
            method="DELETE",
            user_token=user_token
        )

        return {
            "success": result.get("success", False) if isinstance(result, dict) else True,
            "message": "Task deleted successfully"
        }

    async def mark_task_complete(
        self,
        task_id: str,
        completed: bool = True,
        user_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Mark a task as complete or incomplete

        Args:
            task_id: ID of task to update
            completed: True to mark complete, False to mark incomplete
            user_token: User JWT token for authentication

        Returns:
            Dictionary with success status and updated task
        """
        result = await self._call_api(
            endpoint=f"/api/tasks/{task_id}/complete",
            method="PATCH",
            user_token=user_token
        )

        return {
            "success": True if "id" in result else False,
            "task": result if "id" in result else None,
            "message": f"Task marked as {'complete' if completed else 'incomplete'}"
        }

    async def get_task_stats(
        self,
        user_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get task statistics

        Args:
            user_token: User JWT token for authentication

        Returns:
            Dictionary with task statistics
        """
        result = await self._call_api(
            endpoint="/api/tasks",
            method="GET",
            user_token=user_token
        )

        if isinstance(result, list):
            total = len(result)
            completed = sum(1 for t in result if t.get("completed", False))
            active = total - completed
            completion_rate = round((completed / total * 100) if total > 0 else 0, 1)

            return {
                "success": True,
                "stats": {
                    "total": total,
                    "active": active,
                    "completed": completed,
                    "completion_rate": completion_rate
                }
            }

        return {
            "success": False,
            "stats": {},
            "error": "Failed to fetch task statistics"
        }


# Tool definitions for MCP
TOOL_DEFINITIONS = [
    {
        "name": "create_task",
        "description": "Create a new task. Use this when the user wants to add a task.",
        "input_schema": {
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
    },
    {
        "name": "list_tasks",
        "description": "List the user's tasks. Use this when the user asks about their tasks.",
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["all", "active", "completed"],
                    "description": "Filter tasks by status (default: all)"
                }
            }
        }
    },
    {
        "name": "update_task",
        "description": "Update an existing task. Use this when the user wants to modify a task.",
        "input_schema": {
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
    },
    {
        "name": "delete_task",
        "description": "Delete a task. Use this when the user wants to remove a task.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The ID of the task to delete"
                }
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "mark_task_complete",
        "description": "Mark a task as complete or incomplete. Use when user says they finished a task.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The ID of the task"
                },
                "completed": {
                    "type": "boolean",
                    "description": "True to mark complete, False to mark incomplete",
                    "default": True
                }
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "get_task_stats",
        "description": "Get statistics about the user's tasks. Use when user asks about their progress.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    }
]
