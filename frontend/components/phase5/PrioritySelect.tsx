"use client";

interface PrioritySelectProps {
  value: "high" | "medium" | "low";
  onChange: (priority: "high" | "medium" | "low") => void;
  label?: string;
}

export default function PrioritySelect({ value, onChange, label }: PrioritySelectProps) {
  return (
    <div className="space-y-1">
      {label && (
        <label className="block text-sm font-medium text-gray-700">
          {label}
        </label>
      )}
      <select
        value={value}
        onChange={(e) => onChange(e.target.value as "high" | "medium" | "low")}
        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
      >
        <option value="high">⚠️ High Priority</option>
        <option value="medium">📌 Medium Priority</option>
        <option value="low">✓ Low Priority</option>
      </select>
    </div>
  );
}
