/**
 * API Client for TaskFlow Backend
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
}

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority?: string;
  tags?: string[];
  due_date?: string;
  reminder_date?: string;
  is_recurring?: boolean;
  recurrence_pattern?: any;
  parent_task_id?: number;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}

class APIClient {
  private getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('token');
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getToken();

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    if (response.status === 204) {
      return null as T;
    }

    return response.json();
  }

  // Auth endpoints
  async signup(name: string, email: string, password: string): Promise<AuthResponse> {
    return this.request<AuthResponse>('/api/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ name, email, password }),
    });
  }

  async login(email: string, password: string): Promise<AuthResponse> {
    return this.request<AuthResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  // Task endpoints
  async getTasks(filters?: {
    completed?: boolean | null;
    priority?: string;
    tags?: string;
    search?: string;
    sortBy?: string;
    sortOrder?: string;
  }): Promise<{ tasks: Task[]; total: number; count: number }> {
    const params = new URLSearchParams();

    if (filters?.completed !== null && filters?.completed !== undefined) {
      params.append('completed', String(filters.completed));
    }
    if (filters?.priority) params.append('priority', filters.priority);
    if (filters?.tags) params.append('tags', filters.tags);
    if (filters?.search) params.append('search', filters.search);
    if (filters?.sortBy) params.append('sort_by', filters.sortBy);
    if (filters?.sortOrder) params.append('sort_order', filters.sortOrder);

    const queryString = params.toString();
    return this.request<{ tasks: Task[]; total: number; count: number }>(
      `/api/tasks${queryString ? `?${queryString}` : ''}`
    );
  }

  async createTask(taskData: {
    title: string;
    description?: string;
    priority?: string;
    tags?: string[];
    due_date?: string;
    reminder_date?: string;
    is_recurring?: boolean;
    recurrence_pattern?: any;
  }): Promise<Task> {
    return this.request<Task>('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(
    id: number,
    data: { title?: string; description?: string; completed?: boolean }
  ): Promise<Task> {
    return this.request<Task>(`/api/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async toggleTaskComplete(id: number): Promise<Task> {
    return this.request<Task>(`/api/tasks/${id}/complete`, {
      method: 'PATCH',
    });
  }

  async deleteTask(id: number): Promise<void> {
    return this.request<void>(`/api/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  // Generic HTTP methods for additional endpoints
  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

export const api = new APIClient();
export const apiClient = api; // Alias for compatibility
