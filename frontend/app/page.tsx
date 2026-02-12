'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import AuthGuard from '@/components/AuthGuard';
import TaskFormEnhanced from '@/components/TaskFormEnhanced';
import TaskList from '@/components/TaskList';
import TaskStatistics from '@/components/TaskStatistics';
import ProgressChart from '@/components/ProgressChart';
import TaskFilters from '@/components/TaskFilters';
import Chatbot from '@/components/Chatbot';
import { api, Task } from '@/lib/api';
import { LogOut, RefreshCw, User, Menu, X } from 'lucide-react';

function DashboardContent() {
  const { user, logout } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState<any>({});

  const fetchTasks = async (customFilters?: any) => {
    try {
      setError('');
      const response = await api.getTasks(customFilters || filters);
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

  const handleFilterChange = (newFilters: any) => {
    setFilters(newFilters);
    fetchTasks(newFilters);
  };

  const handleCreateTask = async (taskData: any) => {
    const newTask = await api.createTask(taskData);
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
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 pb-20 md:pb-8">
      <div className="max-w-4xl mx-auto px-3 md:px-4 py-4 md:py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8 flex-wrap gap-4">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-white mb-1">TaskFlow</h1>
            <p className="text-gray-400 text-sm md:text-base">Welcome, {user?.name}!</p>
          </div>

          {/* Desktop Actions */}
          <div className="hidden md:flex items-center gap-3">
            <button
              onClick={fetchTasks}
              className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-colors border border-white/20"
              title="Refresh tasks"
            >
              <RefreshCw size={18} />
              <span>Refresh</span>
            </button>
            <button
              onClick={logout}
              className="flex items-center gap-2 px-4 py-2 bg-red-600/80 hover:bg-red-600 text-white rounded-lg transition-colors"
              title="Logout"
            >
              <LogOut size={18} />
              <span>Logout</span>
            </button>
          </div>

          {/* Mobile Actions */}
          <div className="flex md:hidden items-center gap-2">
            <button
              onClick={fetchTasks}
              className="p-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-colors border border-white/20"
              title="Refresh"
            >
              <RefreshCw size={20} />
            </button>
            <button
              onClick={logout}
              className="p-2 bg-red-600/80 hover:bg-red-600 text-white rounded-lg transition-colors"
              title="Logout"
            >
              <LogOut size={20} />
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

        {/* Task Filters */}
        <TaskFilters onFilterChange={handleFilterChange} />

        {/* Task Form */}
        <div className="mb-8">
          <TaskFormEnhanced onSubmit={handleCreateTask} />
        </div>

        {/* Task List */}
        {loading ? (
          <div className="text-center py-16 md:py-20">
            <div className="inline-block">
              <div className="w-12 h-12 md:w-16 md:h-16 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin mb-4"></div>
              <p className="text-gray-400 text-sm md:text-base">Loading your tasks...</p>
            </div>
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

      {/* AI Chatbot */}
      <Chatbot />
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
