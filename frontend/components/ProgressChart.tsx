'use client';

import { Task } from '@/lib/api';

interface ProgressChartProps {
  tasks: Task[];
}

export default function ProgressChart({ tasks }: ProgressChartProps) {
  const total = tasks.length;
  const completed = tasks.filter(t => t.completed).length;
  const completionRate = total > 0 ? Math.round((completed / total) * 100) : 0;

  if (total === 0) {
    return null;
  }

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-6 mb-8">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-white">Overall Progress</h3>
          <p className="text-gray-400 text-sm">
            {completed} of {total} tasks completed
          </p>
        </div>
        <div className="text-3xl font-bold text-purple-400">
          {completionRate}%
        </div>
      </div>

      {/* Progress Bar */}
      <div className="relative w-full h-4 bg-gray-700 rounded-full overflow-hidden">
        <div
          className="absolute top-0 left-0 h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-500 ease-out"
          style={{ width: `${completionRate}%` }}
        >
          <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
        </div>
      </div>

      {/* Completion Message */}
      {completionRate === 100 && total > 0 && (
        <div className="mt-4 text-center">
          <p className="text-green-400 font-semibold text-lg">
            🎉 All tasks completed! Great job!
          </p>
        </div>
      )}
    </div>
  );
}
