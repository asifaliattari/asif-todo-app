'use client';

import { useState } from 'react';
import { Plus, Calendar, Tag as TagIcon, Clock, Repeat, Bell } from 'lucide-react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

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
  const [dueDate, setDueDate] = useState<Date | null>(null);
  const [reminderDate, setReminderDate] = useState<Date | null>(null);
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
        taskData.due_date = dueDate.toISOString();
      }

      if (reminderDate) {
        taskData.reminder_date = reminderDate.toISOString();
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
      setDueDate(null);
      setReminderDate(null);
      setIsRecurring(false);
      setShowAdvanced(false);
    } catch (error) {
      console.error('Failed to create task:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-gray-800 p-4 md:p-6 rounded-lg shadow-lg border border-gray-700">
      {/* Title */}
      <div>
        <input
          type="text"
          placeholder="What needs to be done?"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-3 md:px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white text-sm md:text-base placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all"
          disabled={loading}
          autoFocus
        />
      </div>

      {/* Description */}
      <div>
        <textarea
          placeholder="Add more details (optional)..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="w-full px-3 md:px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white text-sm md:text-base placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 resize-none transition-all"
          disabled={loading}
        />
      </div>

      {/* Priority & Advanced Toggle */}
      <div className="flex gap-2 md:gap-3">
        <div className="flex-1">
          <label className="block text-sm text-gray-400 mb-2">Priority</label>
          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            className="w-full px-3 md:px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white text-sm md:text-base focus:outline-none focus:ring-2 focus:ring-purple-500"
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
            className={`px-3 md:px-4 py-2 rounded-lg transition-all text-sm md:text-base whitespace-nowrap ${
              showAdvanced
                ? 'bg-purple-600 text-white shadow-lg'
                : 'bg-gray-700 hover:bg-gray-600 text-white'
            }`}
          >
            {showAdvanced ? '− Less' : '+ More'}
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
              Due Date & Time
            </label>
            <DatePicker
              selected={dueDate}
              onChange={(date: Date | null) => setDueDate(date)}
              showTimeSelect
              timeFormat="HH:mm"
              timeIntervals={15}
              dateFormat="MMMM d, yyyy h:mm aa"
              placeholderText="Click to select date & time"
              disabled={loading}
              className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
              calendarClassName="bg-gray-800 border-gray-700"
              minDate={new Date()}
            />
          </div>

          {/* Reminder Date & Time */}
          <div>
            <label className="flex items-center gap-2 text-sm text-gray-400 mb-2">
              <Bell size={16} />
              Reminder Alert
              <span className="text-xs text-gray-500">(Get email notification)</span>
            </label>
            <DatePicker
              selected={reminderDate}
              onChange={(date: Date | null) => setReminderDate(date)}
              showTimeSelect
              timeFormat="HH:mm"
              timeIntervals={15}
              dateFormat="MMMM d, yyyy h:mm aa"
              placeholderText="When to remind you?"
              disabled={loading}
              className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              calendarClassName="bg-gray-800 border-gray-700"
              minDate={new Date()}
            />
            <p className="text-xs text-gray-500 mt-1">
              💡 Tip: Set reminder before due date (e.g., 1 hour before, 1 day before)
            </p>
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

      {/* Submit Button - Highlighted */}
      <div className="relative">
        {/* Animated ring for emphasis */}
        {!loading && title.trim() && (
          <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg opacity-75 blur animate-pulse"></div>
        )}

        <button
          type="submit"
          disabled={loading || !title.trim()}
          className="relative w-full flex items-center justify-center gap-2 px-4 py-4 bg-gradient-to-r from-purple-600 via-purple-500 to-pink-600 hover:from-purple-700 hover:via-purple-600 hover:to-pink-700 text-white font-bold rounded-lg transition-all shadow-2xl hover:shadow-purple-500/60 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:shadow-none transform hover:scale-[1.03] active:scale-[0.97] text-lg border-2 border-white/10"
        >
          {/* Shine effect */}
          <div className="absolute inset-0 rounded-lg overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full animate-shimmer"></div>
          </div>

          {loading ? (
            <>
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
              <span>Adding Task...</span>
            </>
          ) : (
            <>
              <Plus size={22} className="font-bold" />
              <span>Add Task</span>
              <span className="text-xl">✨</span>
            </>
          )}
        </button>
      </div>

      <style jsx>{`
        @keyframes shimmer {
          0% {
            transform: translateX(-100%);
          }
          100% {
            transform: translateX(100%);
          }
        }
        .animate-shimmer {
          animation: shimmer 3s infinite;
        }
      `}</style>
    </form>
  );
}
