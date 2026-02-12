'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import AuthGuard from '@/components/AuthGuard';
import TaskForm from '@/components/TaskForm';
import TaskList from '@/components/TaskList';
import TaskStatistics from '@/components/TaskStatistics';
import ProgressChart from '@/components/ProgressChart';
import { api, Task } from '@/lib/api';
import { LogOut, RefreshCw } from 'lucide-react';

function DashboardContent() {
  const { user, logout } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchTasks = async () => {
    try {
      setError('');
      const response = await api.getTasks();
      setTasks(response.tasks);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleCreateTask = async (title: string, description: string) => {
    const newTask = await api.createTask(title, description);
    setTasks([newTask, ...tasks]);
  };

  const handleToggleTask = async (id: number) => {
    const updatedTask = await api.toggleTaskComplete(id);
    setTasks(tasks.map(t => t.id === id ? updatedTask : t));
  };

  const handleDeleteTask = async (id: number) => {
    await api.deleteTask(id);
    setTasks(tasks.filter(t => t.id !== id));
  };

  const handleUpdateTask = async (id: number, title: string, description: string) => {
    const updatedTask = await api.updateTask(id, { title, description });
    setTasks(tasks.map(t => t.id === id ? updatedTask : t));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">TaskFlow</h1>
            <p className="text-gray-400">Welcome back, {user?.name}!</p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={fetchTasks}
              className="flex items-center gap-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
            >
              <RefreshCw size={18} />
              Refresh
            </button>
            <button
              onClick={logout}
              className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
            >
              <LogOut size={18} />
              Logout
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-500/10 border border-red-500 text-red-500 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Task Statistics */}
        {!loading && <TaskStatistics tasks={tasks} />}

        {/* Progress Chart */}
        {!loading && <ProgressChart tasks={tasks} />}

        {/* Task Form */}
        <div className="mb-8">
          <TaskForm onSubmit={handleCreateTask} />
        </div>

        {/* Task List */}
        {loading ? (
          <div className="text-center py-12">
            <div className="text-white text-xl">Loading tasks...</div>
          </div>
        ) : (
          <TaskList
            tasks={tasks}
            onToggle={handleToggleTask}
            onDelete={handleDeleteTask}
            onUpdate={handleUpdateTask}
          />
        )}

        {/* Footer */}
        <div className="mt-12 text-center">
          <p className="text-gray-500 text-sm">
            Created by Asif Ali AstolixGen | GIAIC Hackathon 2026
          </p>
        </div>
      </div>
    </div>
  );
}

export default function Dashboard() {
  return (
    <AuthGuard>
      <DashboardContent />
    </AuthGuard>
  );
}
