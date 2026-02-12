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
    <div className="bg-gradient-to-br from-gray-800/80 to-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-lg p-4 md:p-6 mb-6 md:mb-8 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base md:text-lg font-semibold text-white flex items-center gap-2">
            📊 Overall Progress
          </h3>
          <p className="text-gray-400 text-xs md:text-sm">
            {completed} of {total} tasks completed
          </p>
        </div>
        <div className="text-2xl md:text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
          {completionRate}%
        </div>
      </div>

      {/* Progress Bar */}
      <div className="relative w-full h-3 md:h-4 bg-gray-700/50 rounded-full overflow-hidden shadow-inner">
        <div
          className="absolute top-0 left-0 h-full bg-gradient-to-r from-purple-500 via-purple-400 to-pink-500 transition-all duration-700 ease-out shadow-lg"
          style={{ width: `${completionRate}%` }}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-white/30 to-transparent animate-pulse"></div>
          <div className="absolute inset-0 bg-gradient-to-b from-white/20 to-transparent"></div>
        </div>
      </div>

      {/* Completion Message */}
      {completionRate === 100 && total > 0 && (
        <div className="mt-4 text-center animate-bounce">
          <p className="text-green-400 font-semibold text-base md:text-lg">
            🎉 All tasks completed! Great job!
          </p>
        </div>
      )}
    </div>
  );
}
