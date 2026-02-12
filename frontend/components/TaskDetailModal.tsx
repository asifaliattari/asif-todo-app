'use client';

import { Task } from '@/lib/api';
import { X, Calendar, Tag as TagIcon, Repeat, CheckCircle2, Circle, Trash2, Pencil } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

interface TaskDetailModalProps {
  task: Task;
  isOpen: boolean;
  onClose: () => void;
  onToggle: (id: number) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  onEdit: () => void;
}

export default function TaskDetailModal({
  task,
  isOpen,
  onClose,
  onToggle,
  onDelete,
  onEdit
}: TaskDetailModalProps) {
  if (!isOpen) return null;

  const handleToggle = async () => {
    await onToggle(task.id);
  };

  const handleDelete = async () => {
    if (confirm('Are you sure you want to delete this task?')) {
      await onDelete(task.id);
      onClose();
    }
  };

  const handleEdit = () => {
    onEdit();
    onClose();
  };

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 animate-fadeIn"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div
          className="bg-gray-800 border border-gray-700 rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto animate-slideUp"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="sticky top-0 bg-gradient-to-r from-purple-600 to-pink-600 p-6 rounded-t-2xl">
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-start gap-3 flex-1">
                <button
                  onClick={handleToggle}
                  className="mt-1 text-white hover:scale-110 transition-transform flex-shrink-0"
                >
                  {task.completed ? (
                    <CheckCircle2 size={28} />
                  ) : (
                    <Circle size={28} />
                  )}
                </button>
                <div className="flex-1">
                  <h2 className={`text-2xl font-bold text-white mb-2 ${task.completed ? 'line-through opacity-75' : ''}`}>
                    {task.title}
                  </h2>
                  {task.priority && (
                    <span
                      className={`inline-block px-3 py-1 text-sm rounded-full font-semibold ${
                        task.priority === 'high'
                          ? 'bg-red-500/90 text-white'
                          : task.priority === 'low'
                          ? 'bg-green-500/90 text-white'
                          : 'bg-yellow-500/90 text-white'
                      }`}
                    >
                      {task.priority === 'high' ? '🔴 High Priority' :
                       task.priority === 'low' ? '🟢 Low Priority' : '🟡 Medium Priority'}
                    </span>
                  )}
                </div>
              </div>
              <button
                onClick={onClose}
                className="text-white/80 hover:text-white hover:bg-white/10 p-2 rounded-lg transition-colors flex-shrink-0"
              >
                <X size={24} />
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="p-6 space-y-6">
            {/* Description */}
            {task.description && (
              <div>
                <h3 className="text-sm font-semibold text-gray-400 mb-2">Description</h3>
                <p className="text-white text-base leading-relaxed">{task.description}</p>
              </div>
            )}

            {/* Tags */}
            {task.tags && task.tags.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold text-gray-400 mb-2 flex items-center gap-2">
                  <TagIcon size={16} />
                  Tags
                </h3>
                <div className="flex flex-wrap gap-2">
                  {task.tags.map((tag, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1.5 bg-purple-500/20 text-purple-300 text-sm rounded-full border border-purple-500/30 font-medium"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Dates */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {task.due_date && (
                <div className="bg-gray-900/50 border border-gray-700 rounded-lg p-4">
                  <h3 className="text-sm font-semibold text-gray-400 mb-2 flex items-center gap-2">
                    <Calendar size={16} />
                    Due Date
                  </h3>
                  <p className={`text-base font-medium ${
                    new Date(task.due_date) < new Date() && !task.completed
                      ? 'text-red-400'
                      : 'text-blue-400'
                  }`}>
                    {new Date(task.due_date).toLocaleDateString('en-US', {
                      weekday: 'long',
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </p>
                  {new Date(task.due_date) < new Date() && !task.completed && (
                    <p className="text-red-400 text-sm mt-1 font-semibold">⚠️ Overdue</p>
                  )}
                </div>
              )}

              <div className="bg-gray-900/50 border border-gray-700 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-gray-400 mb-2">Created</h3>
                <p className="text-base font-medium text-gray-300">
                  {formatDistanceToNow(new Date(task.created_at), { addSuffix: true })}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  {new Date(task.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>

            {/* Recurring */}
            {task.is_recurring && (
              <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-purple-400 mb-2 flex items-center gap-2">
                  <Repeat size={16} />
                  Recurring Task
                </h3>
                <p className="text-purple-300">
                  This task repeats automatically
                </p>
              </div>
            )}

            {/* Status */}
            <div className={`rounded-lg p-4 ${
              task.completed
                ? 'bg-green-500/10 border border-green-500/30'
                : 'bg-yellow-500/10 border border-yellow-500/30'
            }`}>
              <p className={`font-semibold ${
                task.completed ? 'text-green-400' : 'text-yellow-400'
              }`}>
                {task.completed ? '✅ Task Completed' : '⏳ Task Pending'}
              </p>
            </div>
          </div>

          {/* Actions */}
          <div className="sticky bottom-0 bg-gray-800 border-t border-gray-700 p-6 rounded-b-2xl">
            <div className="flex gap-3">
              <button
                onClick={handleEdit}
                className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors"
              >
                <Pencil size={18} />
                Edit Task
              </button>
              <button
                onClick={handleDelete}
                className="flex items-center justify-center gap-2 px-4 py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition-colors"
              >
                <Trash2 size={18} />
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>

      <style jsx global>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fadeIn {
          animation: fadeIn 0.2s ease-out;
        }
        .animate-slideUp {
          animation: slideUp 0.3s ease-out;
        }
      `}</style>
    </>
  );
}
