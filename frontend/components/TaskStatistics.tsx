'use client';

import { Task } from '@/lib/api';
import { CheckCircle2, Clock, ListTodo, TrendingUp } from 'lucide-react';

interface TaskStatisticsProps {
  tasks: Task[];
  onFilterClick?: (filter: 'all' | 'completed' | 'pending') => void;
}

export default function TaskStatistics({ tasks, onFilterClick }: TaskStatisticsProps) {
  const total = tasks.length;
  const completed = tasks.filter(t => t.completed).length;
  const pending = total - completed;
  const completionRate = total > 0 ? Math.round((completed / total) * 100) : 0;

  const stats = [
    {
      label: 'Total Tasks',
      value: total,
      icon: ListTodo,
      color: 'text-blue-400',
      bgColor: 'bg-blue-400/10',
      borderColor: 'border-blue-400/20',
      hoverColor: 'hover:bg-blue-400/20',
      filter: 'all' as const
    },
    {
      label: 'Completed',
      value: completed,
      icon: CheckCircle2,
      color: 'text-green-400',
      bgColor: 'bg-green-400/10',
      borderColor: 'border-green-400/20',
      hoverColor: 'hover:bg-green-400/20',
      filter: 'completed' as const
    },
    {
      label: 'Pending',
      value: pending,
      icon: Clock,
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-400/10',
      borderColor: 'border-yellow-400/20',
      hoverColor: 'hover:bg-yellow-400/20',
      filter: 'pending' as const
    },
    {
      label: 'Progress',
      value: `${completionRate}%`,
      icon: TrendingUp,
      color: 'text-purple-400',
      bgColor: 'bg-purple-400/10',
      borderColor: 'border-purple-400/20',
      hoverColor: 'hover:bg-purple-400/20',
      filter: null
    }
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      {stats.map((stat, index) => {
        const Icon = stat.icon;
        const isClickable = stat.filter && onFilterClick;
        return (
          <div
            key={index}
            onClick={() => isClickable && onFilterClick(stat.filter!)}
            className={`${stat.bgColor} ${stat.borderColor} ${stat.hoverColor} border rounded-lg p-4 transition-all ${
              isClickable ? 'cursor-pointer hover:scale-105 hover:shadow-lg' : 'hover:scale-105'
            }`}
            role={isClickable ? 'button' : undefined}
            tabIndex={isClickable ? 0 : undefined}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm mb-1">
                  {stat.label}
                  {isClickable && <span className="ml-2 text-xs opacity-60">▸</span>}
                </p>
                <p className={`${stat.color} text-3xl font-bold`}>
                  {stat.value}
                </p>
              </div>
              <div className={`${stat.color} ${stat.bgColor} p-3 rounded-lg`}>
                <Icon size={24} />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
