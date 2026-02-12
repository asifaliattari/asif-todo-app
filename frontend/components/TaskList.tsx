'use client';

import { Task } from '@/lib/api';
import TaskItem from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  onToggle: (id: number) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  onUpdate: (id: number, title: string, description: string) => Promise<void>;
}

export default function TaskList({ tasks, onToggle, onDelete, onUpdate }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-16 md:py-20">
        <div className="text-6xl md:text-8xl mb-4">📝</div>
        <p className="text-gray-300 text-lg md:text-xl font-medium mb-2">No tasks yet</p>
        <p className="text-gray-500 text-sm md:text-base">Create your first task above to get started!</p>
      </div>
    );
  }

  const activeTasks = tasks.filter(t => !t.completed);
  const completedTasks = tasks.filter(t => t.completed);

  return (
    <div className="space-y-6 md:space-y-8">
      {activeTasks.length > 0 && (
        <div>
          <div className="flex items-center gap-3 mb-4">
            <div className="h-1 w-1 bg-purple-500 rounded-full"></div>
            <h2 className="text-lg md:text-xl font-semibold text-white">
              Active Tasks
            </h2>
            <span className="px-2.5 py-0.5 bg-purple-500/20 text-purple-400 text-sm rounded-full border border-purple-500/30">
              {activeTasks.length}
            </span>
          </div>
          <div className="space-y-2 md:space-y-3">
            {activeTasks.map(task => (
              <TaskItem
                key={task.id}
                task={task}
                onToggle={onToggle}
                onDelete={onDelete}
                onUpdate={onUpdate}
              />
            ))}
          </div>
        </div>
      )}

      {completedTasks.length > 0 && (
        <div>
          <div className="flex items-center gap-3 mb-4">
            <div className="h-1 w-1 bg-green-500 rounded-full"></div>
            <h2 className="text-lg md:text-xl font-semibold text-white">
              Completed Tasks
            </h2>
            <span className="px-2.5 py-0.5 bg-green-500/20 text-green-400 text-sm rounded-full border border-green-500/30">
              {completedTasks.length}
            </span>
          </div>
          <div className="space-y-2 md:space-y-3">
            {completedTasks.map(task => (
              <TaskItem
                key={task.id}
                task={task}
                onToggle={onToggle}
                onDelete={onDelete}
                onUpdate={onUpdate}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
