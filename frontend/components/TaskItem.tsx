'use client';

import { useState } from 'react';
import { Task } from '@/lib/api';
import { CheckCircle2, Circle, Trash2, Pencil, X, Check } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

interface TaskItemProps {
  task: Task;
  onToggle: (id: number) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  onUpdate: (id: number, title: string, description: string) => Promise<void>;
}

export default function TaskItem({ task, onToggle, onDelete, onUpdate }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');
  const [loading, setLoading] = useState(false);

  const handleToggle = async () => {
    setLoading(true);
    try {
      await onToggle(task.id);
    } catch (error) {
      console.error('Failed to toggle task:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) return;

    setLoading(true);
    try {
      await onDelete(task.id);
    } catch (error) {
      console.error('Failed to delete task:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!editTitle.trim()) return;

    setLoading(true);
    try {
      await onUpdate(task.id, editTitle, editDescription);
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to update task:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <div className="bg-gray-800 border border-purple-500/30 rounded-lg p-3 md:p-4 space-y-3 shadow-lg">
        <input
          type="text"
          value={editTitle}
          onChange={(e) => setEditTitle(e.target.value)}
          className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white text-sm md:text-base focus:outline-none focus:ring-2 focus:ring-purple-500"
          disabled={loading}
          placeholder="Task title"
        />
        <textarea
          value={editDescription}
          onChange={(e) => setEditDescription(e.target.value)}
          rows={2}
          className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white text-sm md:text-base focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
          disabled={loading}
          placeholder="Description (optional)"
        />
        <div className="flex gap-2">
          <button
            onClick={handleSave}
            disabled={loading || !editTitle.trim()}
            className="flex items-center gap-1 px-3 py-1.5 bg-green-600 hover:bg-green-700 text-white text-sm rounded-lg transition-colors disabled:opacity-50"
          >
            <Check size={16} />
            <span className="hidden sm:inline">Save</span>
          </button>
          <button
            onClick={handleCancel}
            disabled={loading}
            className="flex items-center gap-1 px-3 py-1.5 bg-gray-600 hover:bg-gray-700 text-white text-sm rounded-lg transition-colors"
          >
            <X size={16} />
            <span className="hidden sm:inline">Cancel</span>
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-lg p-3 md:p-4 transition-all hover:border-purple-500/50 hover:shadow-lg hover:shadow-purple-500/10 ${task.completed ? 'opacity-60' : ''}`}>
      <div className="flex items-start gap-2 md:gap-3">
        <button
          onClick={handleToggle}
          disabled={loading}
          className="mt-0.5 text-purple-400 hover:text-purple-300 hover:scale-110 transition-all disabled:opacity-50 flex-shrink-0"
        >
          {task.completed ? <CheckCircle2 size={22} className="md:w-6 md:h-6" /> : <Circle size={22} className="md:w-6 md:h-6" />}
        </button>

        <div className="flex-1 min-w-0">
          <div className="flex items-start flex-wrap gap-2 mb-1">
            <h3 className={`text-base md:text-lg font-medium text-white ${task.completed ? 'line-through' : ''} break-words`}>
              {task.title}
            </h3>
            {/* Priority Badge */}
            {task.priority && (
              <span className={`px-2 py-0.5 text-xs rounded-full font-medium whitespace-nowrap ${
                task.priority === 'high' ? 'bg-red-500/20 text-red-400 ring-1 ring-red-500/30' :
                task.priority === 'low' ? 'bg-green-500/20 text-green-400 ring-1 ring-green-500/30' :
                'bg-yellow-500/20 text-yellow-400 ring-1 ring-yellow-500/30'
              }`}>
                {task.priority === 'high' ? '🔴 High' :
                 task.priority === 'low' ? '🟢 Low' : '🟡 Medium'}
              </span>
            )}
          </div>

          {task.description && (
            <p className="text-gray-400 text-sm mt-1 break-words">{task.description}</p>
          )}

          {/* Tags */}
          {task.tags && task.tags.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mt-2">
              {task.tags.map((tag, idx) => (
                <span key={idx} className="px-2 py-1 bg-purple-500/20 text-purple-300 text-xs rounded-full border border-purple-500/30">
                  #{tag}
                </span>
              ))}
            </div>
          )}

          {/* Due Date & Created Date */}
          <div className="flex flex-wrap items-center gap-2 md:gap-3 mt-2.5">
            {task.due_date && (
              <p className={`text-xs font-medium flex items-center gap-1 ${
                new Date(task.due_date) < new Date() && !task.completed
                  ? 'text-red-400'
                  : 'text-blue-400'
              }`}>
                <span>📅</span>
                <span className="hidden sm:inline">Due:</span>
                <span>{new Date(task.due_date).toLocaleDateString()}</span>
              </p>
            )}
            {task.is_recurring && (
              <span className="text-xs text-purple-400 font-medium">🔄 Recurring</span>
            )}
            <p className="text-gray-500 text-xs">
              {formatDistanceToNow(new Date(task.created_at), { addSuffix: true })}
            </p>
          </div>
        </div>

        <div className="flex flex-col md:flex-row gap-1 md:gap-2 flex-shrink-0">
          <button
            onClick={() => setIsEditing(true)}
            disabled={loading}
            className="text-blue-400 hover:text-blue-300 hover:scale-110 transition-all disabled:opacity-50 p-1"
            title="Edit task"
          >
            <Pencil size={18} />
          </button>
          <button
            onClick={handleDelete}
            disabled={loading}
            className="text-red-400 hover:text-red-300 hover:scale-110 transition-all disabled:opacity-50 p-1"
            title="Delete task"
          >
            <Trash2 size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
