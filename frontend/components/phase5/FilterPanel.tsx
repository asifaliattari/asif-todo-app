"use client";

interface FilterPanelProps {
  onFilter: (filters: FilterOptions) => void;
  currentFilters: FilterOptions;
}

export interface FilterOptions {
  priority?: "high" | "medium" | "low" | null;
  status?: "all" | "active" | "completed";
  sortBy?: "created_at" | "due_date" | "priority" | "title";
  sortOrder?: "asc" | "desc";
}

export default function FilterPanel({ onFilter, currentFilters }: FilterPanelProps) {
  const updateFilter = (key: keyof FilterOptions, value: any) => {
    onFilter({ ...currentFilters, [key]: value });
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 space-y-4">
      <h3 className="font-semibold text-gray-900">Filters</h3>

      {/* Priority Filter */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Priority
        </label>
        <div className="space-y-1">
          {["all", "high", "medium", "low"].map((priority) => (
            <label key={priority} className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="priority"
                checked={
                  priority === "all"
                    ? !currentFilters.priority
                    : currentFilters.priority === priority
                }
                onChange={() =>
                  updateFilter("priority", priority === "all" ? null : priority)
                }
                className="text-purple-600"
              />
              <span className="text-sm capitalize">{priority}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Status Filter */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Status
        </label>
        <select
          value={currentFilters.status || "all"}
          onChange={(e) => updateFilter("status", e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
        >
          <option value="all">All Tasks</option>
          <option value="active">Active</option>
          <option value="completed">Completed</option>
        </select>
      </div>

      {/* Sort Options */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Sort By
        </label>
        <select
          value={currentFilters.sortBy || "created_at"}
          onChange={(e) => updateFilter("sortBy", e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm mb-2"
        >
          <option value="created_at">Created Date</option>
          <option value="due_date">Due Date</option>
          <option value="priority">Priority</option>
          <option value="title">Title</option>
        </select>

        <select
          value={currentFilters.sortOrder || "desc"}
          onChange={(e) => updateFilter("sortOrder", e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
        >
          <option value="desc">Descending</option>
          <option value="asc">Ascending</option>
        </select>
      </div>

      {/* Clear Filters */}
      <button
        onClick={() => onFilter({})}
        className="w-full px-4 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
      >
        Clear All Filters
      </button>
    </div>
  );
}
