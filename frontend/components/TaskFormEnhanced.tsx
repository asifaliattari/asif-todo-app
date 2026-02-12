'use client';

import { useState } from 'react';
import { Plus, Calendar, Tag as TagIcon, Clock, Repeat } from 'lucide-react';

interface TaskFormEnhancedProps {
  onSubmit: (data: {
    title: string;
    description: string;
    priority?: string;
    tags?: string[];
    due_date?: string;
    is_recurring?: boolean;
    recurrence_pattern?: any;
  }) => Promise<void>;
}

export default function TaskFormEnhanced({ onSubmit }: TaskFormEnhancedProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('medium');
  const [tags, setTags] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [isRecurring, setIsRecurring] = useState(false);
  const [recurrenceType, setRecurrenceType] = useState('weekly');
  const [loading, setLoading] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setLoading(true);
    try {
      const taskData: any = {
        title,
        description,
        priority,
        tags: tags ? tags.split(',').map(t => t.trim()).filter(Boolean) : [],
      };

      if (dueDate) {
        taskData.due_date = new Date(dueDate).toISOString();
      }

      if (isRecurring) {
        taskData.is_recurring = true;
        taskData.recurrence_pattern = {
          type: recurrenceType,
          interval: 1
        };
      }

      await onSubmit(taskData);

      // Reset form
      setTitle('');
      setDescription('');
      setPriority('medium');
      setTags('');
      setDueDate('');
      setIsRecurring(false);
      setShowAdvanced(false);
    } catch (error) {
      console.error('Failed to create task:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
      {/* Title */}
      <div>
        <input
          type="text"
          placeholder="Task title..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
          disabled={loading}
        />
      </div>

      {/* Description */}
      <div>
        <textarea
          placeholder="Description (optional)..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
          disabled={loading}
        />
      </div>

      {/* Priority & Advanced Toggle */}
      <div className="flex gap-3">
        <div className="flex-1">
          <label className="block text-sm text-gray-400 mb-2">Priority</label>
          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
            disabled={loading}
          >
            <option value="low">🟢 Low</option>
            <option value="medium">🟡 Medium</option>
            <option value="high">🔴 High</option>
          </select>
        </div>
        <div className="flex items-end">
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
          >
            {showAdvanced ? 'Less' : 'More'} Options
          </button>
        </div>
      </div>

      {/* Advanced Options */}
      {showAdvanced && (
        <div className="space-y-4 pt-4 border-t border-gray-700">
          {/* Tags */}
          <div>
            <label className="flex items-center gap-2 text-sm text-gray-400 mb-2">
              <TagIcon size={16} />
              Tags (comma-separated)
            </label>
            <input
              type="text"
              placeholder="work, urgent, meeting"
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
              disabled={loading}
            />
          </div>

          {/* Due Date */}
          <div>
            <label className="flex items-center gap-2 text-sm text-gray-400 mb-2">
              <Calendar size={16} />
              Due Date
            </label>
            <input
              type="datetime-local"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
              disabled={loading}
            />
          </div>

          {/* Recurring */}
          <div className="flex items-center gap-4">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={isRecurring}
                onChange={(e) => setIsRecurring(e.target.checked)}
                className="w-4 h-4 text-purple-600 bg-gray-900 border-gray-700 rounded focus:ring-purple-500"
                disabled={loading}
              />
              <Repeat size={16} className="text-gray-400" />
              <span className="text-gray-400">Recurring Task</span>
            </label>

            {isRecurring && (
              <select
                value={recurrenceType}
                onChange={(e) => setRecurrenceType(e.target.value)}
                className="px-3 py-1 bg-gray-900 border border-gray-700 rounded text-white text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
                disabled={loading}
              >
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            )}
          </div>
        </div>
      )}

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading || !title.trim()}
        className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Plus size={20} />
        {loading ? 'Adding...' : 'Add Task'}
      </button>
    </form>
  );
}
