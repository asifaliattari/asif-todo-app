'use client';

import { useState } from 'react';
import { Search, Filter, SortAsc, X } from 'lucide-react';

interface TaskFiltersProps {
  onFilterChange: (filters: {
    search?: string;
    priority?: string;
    tags?: string;
    completed?: boolean | null;
    sortBy?: string;
    sortOrder?: string;
  }) => void;
}

export default function TaskFilters({ onFilterChange }: TaskFiltersProps) {
  const [search, setSearch] = useState('');
  const [priority, setPriority] = useState('');
  const [completedFilter, setCompletedFilter] = useState<string>('all');
  const [sortBy, setSortBy] = useState('created_at');
  const [sortOrder, setSortOrder] = useState('desc');
  const [showFilters, setShowFilters] = useState(false);

  const applyFilters = () => {
    const filters: any = {
      search: search || undefined,
      priority: priority || undefined,
      completed: completedFilter === 'all' ? null : completedFilter === 'completed',
      sortBy,
      sortOrder
    };
    onFilterChange(filters);
  };

  const clearFilters = () => {
    setSearch('');
    setPriority('');
    setCompletedFilter('all');
    setSortBy('created_at');
    setSortOrder('desc');
    onFilterChange({});
  };

  const handleSearchChange = (value: string) => {
    setSearch(value);
    // Auto-search on type
    setTimeout(() => {
      applyFilters();
    }, 300);
  };

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-4 mb-6">
      {/* Search Bar */}
      <div className="flex gap-3">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Search tasks..."
            value={search}
            onChange={(e) => handleSearchChange(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>
        <button
          onClick={() => setShowFilters(!showFilters)}
          className={`px-4 py-2 rounded-lg transition-colors flex items-center gap-2 ${
            showFilters ? 'bg-purple-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          }`}
        >
          <Filter size={18} />
          Filters
        </button>
      </div>

      {/* Advanced Filters */}
      {showFilters && (
        <div className="mt-4 pt-4 border-t border-gray-700 grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Priority Filter */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">Priority</label>
            <select
              value={priority}
              onChange={(e) => {
                setPriority(e.target.value);
                applyFilters();
              }}
              className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="">All Priorities</option>
              <option value="high">🔴 High</option>
              <option value="medium">🟡 Medium</option>
              <option value="low">🟢 Low</option>
            </select>
          </div>

          {/* Status Filter */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">Status</label>
            <select
              value={completedFilter}
              onChange={(e) => {
                setCompletedFilter(e.target.value);
                applyFilters();
              }}
              className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="all">All Tasks</option>
              <option value="active">Active Only</option>
              <option value="completed">Completed Only</option>
            </select>
          </div>

          {/* Sort By */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">Sort By</label>
            <select
              value={sortBy}
              onChange={(e) => {
                setSortBy(e.target.value);
                applyFilters();
              }}
              className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="created_at">Date Created</option>
              <option value="due_date">Due Date</option>
              <option value="priority">Priority</option>
              <option value="title">Title (A-Z)</option>
            </select>
          </div>

          {/* Sort Order */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">Order</label>
            <select
              value={sortOrder}
              onChange={(e) => {
                setSortOrder(e.target.value);
                applyFilters();
              }}
              className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="desc">Newest First</option>
              <option value="asc">Oldest First</option>
            </select>
          </div>

          {/* Clear Filters Button */}
          <div className="md:col-span-4">
            <button
              onClick={clearFilters}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors flex items-center gap-2"
            >
              <X size={16} />
              Clear All Filters
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
