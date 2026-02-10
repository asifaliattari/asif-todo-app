"use client";

interface PriorityBadgeProps {
  priority: "high" | "medium" | "low";
  size?: "sm" | "md" | "lg";
}

export default function PriorityBadge({ priority, size = "sm" }: PriorityBadgeProps) {
  const colors = {
    high: "bg-red-100 text-red-800 border-red-200",
    medium: "bg-yellow-100 text-yellow-800 border-yellow-200",
    low: "bg-green-100 text-green-800 border-green-200",
  };

  const sizes = {
    sm: "text-xs px-2 py-0.5",
    md: "text-sm px-3 py-1",
    lg: "text-base px-4 py-1.5",
  };

  const icons = {
    high: "⚠️",
    medium: "📌",
    low: "✓",
  };

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full border font-medium ${colors[priority]} ${sizes[size]}`}
    >
      <span>{icons[priority]}</span>
      {priority.charAt(0).toUpperCase() + priority.slice(1)}
    </span>
  );
}
