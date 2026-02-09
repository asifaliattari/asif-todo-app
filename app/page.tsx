"use client";

import { useState, useEffect } from "react";
import {
  Plus,
  Trash2,
  Check,
  Clock,
  Filter,
  Search,
  Mic,
  Volume2,
  Star,
  Calendar,
  Tag,
  User,
} from "lucide-react";
import { format } from "date-fns";
import Chatbot from "@/components/Chatbot";

interface Task {
  id: string;
  title: string;
  description?: string;
  priority: "low" | "medium" | "high";
  status: "pending" | "in-progress" | "completed";
  dueDate?: string;
  tags?: string[];
  createdAt: string;
}

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [newTaskDescription, setNewTaskDescription] = useState("");
  const [newTaskPriority, setNewTaskPriority] = useState<"low" | "medium" | "high">("medium");
  const [newTaskDueDate, setNewTaskDueDate] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [filterPriority, setFilterPriority] = useState<string>("all");
  const [filterStatus, setFilterStatus] = useState<string>("all");
  const [isListening, setIsListening] = useState(false);

  // Load tasks from localStorage
  useEffect(() => {
    const savedTasks = localStorage.getItem("tasks");
    if (savedTasks) {
      setTasks(JSON.parse(savedTasks));
    }
  }, []);

  // Save tasks to localStorage
  useEffect(() => {
    if (tasks.length > 0) {
      localStorage.setItem("tasks", JSON.stringify(tasks));
    }
  }, [tasks]);

  const addTask = () => {
    if (!newTaskTitle.trim()) return;

    const newTask: Task = {
      id: Date.now().toString(),
      title: newTaskTitle,
      description: newTaskDescription,
      priority: newTaskPriority,
      status: "pending",
      dueDate: newTaskDueDate || undefined,
      tags: [],
      createdAt: new Date().toISOString(),
    };

    setTasks([newTask, ...tasks]);
    setNewTaskTitle("");
    setNewTaskDescription("");
    setNewTaskPriority("medium");
    setNewTaskDueDate("");
  };

  const deleteTask = (id: string) => {
    setTasks(tasks.filter((task) => task.id !== id));
  };

  const toggleTaskStatus = (id: string) => {
    setTasks(
      tasks.map((task) =>
        task.id === id
          ? {
              ...task,
              status: task.status === "completed" ? "pending" : "completed",
            }
          : task
      )
    );
  };

  const startVoiceRecognition = () => {
    if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.lang = "en-US";
      recognition.continuous = false;

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setNewTaskTitle(transcript);
        setIsListening(false);
      };

      recognition.onerror = () => {
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.start();
    } else {
      alert("Voice recognition is not supported in your browser.");
    }
  };

  const speakText = (text: string) => {
    if ("speechSynthesis" in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = "en-US";
      window.speechSynthesis.speak(utterance);
    }
  };

  const handleChatbotCommand = (command: string) => {
    const lowerCommand = command.toLowerCase();

    // Extract task details from natural language
    if (lowerCommand.includes("add") || lowerCommand.includes("create")) {
      // Extract task title (remove command words)
      let taskTitle = command
        .replace(/add|create|new task|task/gi, "")
        .trim();

      // Detect priority
      let priority: "low" | "medium" | "high" = "medium";
      if (lowerCommand.includes("high priority") || lowerCommand.includes("urgent")) {
        priority = "high";
        taskTitle = taskTitle.replace(/high priority|urgent/gi, "").trim();
      } else if (lowerCommand.includes("low priority")) {
        priority = "low";
        taskTitle = taskTitle.replace(/low priority/gi, "").trim();
      }

      // Create the task if we have a title
      if (taskTitle) {
        const newTask: Task = {
          id: Date.now().toString(),
          title: taskTitle,
          priority: priority,
          status: "pending",
          createdAt: new Date().toISOString(),
        };
        setTasks([newTask, ...tasks]);
      }
    }
  };

  const filteredTasks = tasks.filter((task) => {
    const matchesSearch = task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      task.description?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesPriority = filterPriority === "all" || task.priority === filterPriority;
    const matchesStatus = filterStatus === "all" || task.status === filterStatus;
    return matchesSearch && matchesPriority && matchesStatus;
  });

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "high":
        return "bg-red-500/20 text-red-400 border-red-500/30";
      case "medium":
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30";
      case "low":
        return "bg-green-500/20 text-green-400 border-green-500/30";
      default:
        return "bg-gray-500/20 text-gray-400 border-gray-500/30";
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "bg-emerald-500/20 text-emerald-400 border-emerald-500/30";
      case "in-progress":
        return "bg-blue-500/20 text-blue-400 border-blue-500/30";
      default:
        return "bg-gray-500/20 text-gray-400 border-gray-500/30";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-black text-white">
      {/* Header */}
      <header className="bg-gray-900/50 backdrop-blur-lg border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                TaskFlow
              </h1>
              <p className="text-gray-400 mt-1 flex items-center gap-2">
                <User className="w-4 h-4" />
                by Asif Ali AstolixGen - PIAIC Hackathon
              </p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm text-gray-400">Total Tasks</p>
                <p className="text-2xl font-bold text-blue-400">{tasks.length}</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-400">Completed</p>
                <p className="text-2xl font-bold text-emerald-400">
                  {tasks.filter((t) => t.status === "completed").length}
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Add Task Section */}
        <div className="bg-gray-900/50 backdrop-blur-lg rounded-2xl shadow-2xl border border-gray-800 p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
            <Plus className="w-6 h-6 text-blue-400" />
            Add New Task
          </h2>
          <div className="space-y-4">
            <div className="flex gap-2">
              <input
                type="text"
                value={newTaskTitle}
                onChange={(e) => setNewTaskTitle(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && addTask()}
                placeholder="Task title..."
                className="flex-1 bg-gray-800/50 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
              />
              <button
                onClick={startVoiceRecognition}
                className={`p-3 rounded-lg transition-all ${
                  isListening
                    ? "bg-red-500 hover:bg-red-600 animate-pulse"
                    : "bg-gray-800 hover:bg-gray-700 border border-gray-700"
                }`}
                title="Voice input"
              >
                <Mic className="w-5 h-5" />
              </button>
            </div>
            <textarea
              value={newTaskDescription}
              onChange={(e) => setNewTaskDescription(e.target.value)}
              placeholder="Task description (optional)..."
              className="w-full bg-gray-800/50 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 resize-none"
              rows={2}
            />
            <div className="flex gap-4 flex-wrap">
              <div className="flex items-center gap-2">
                <Star className="w-4 h-4 text-gray-400" />
                <select
                  value={newTaskPriority}
                  onChange={(e) => setNewTaskPriority(e.target.value as any)}
                  className="bg-gray-800/50 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                >
                  <option value="low">Low Priority</option>
                  <option value="medium">Medium Priority</option>
                  <option value="high">High Priority</option>
                </select>
              </div>
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4 text-gray-400" />
                <input
                  type="datetime-local"
                  value={newTaskDueDate}
                  onChange={(e) => setNewTaskDueDate(e.target.value)}
                  className="bg-gray-800/50 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                />
              </div>
              <button
                onClick={addTask}
                className="ml-auto bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-6 py-2 rounded-lg font-medium transition-all flex items-center gap-2 shadow-lg shadow-blue-500/20"
              >
                <Plus className="w-5 h-5" />
                Add Task
              </button>
            </div>
          </div>
        </div>

        {/* Search and Filter */}
        <div className="bg-gray-900/50 backdrop-blur-lg rounded-2xl shadow-2xl border border-gray-800 p-6 mb-8">
          <div className="flex gap-4 flex-wrap">
            <div className="flex-1 min-w-[200px] relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search tasks..."
                className="w-full bg-gray-800/50 border border-gray-700 rounded-lg pl-10 pr-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
              />
            </div>
            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-gray-400" />
              <select
                value={filterPriority}
                onChange={(e) => setFilterPriority(e.target.value)}
                className="bg-gray-800/50 border border-gray-700 rounded-lg px-3 py-3 text-white focus:outline-none focus:border-blue-500"
              >
                <option value="all">All Priorities</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>
            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-gray-400" />
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="bg-gray-800/50 border border-gray-700 rounded-lg px-3 py-3 text-white focus:outline-none focus:border-blue-500"
              >
                <option value="all">All Status</option>
                <option value="pending">Pending</option>
                <option value="in-progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>
          </div>
        </div>

        {/* Tasks List */}
        <div className="space-y-4">
          {filteredTasks.length === 0 ? (
            <div className="bg-gray-900/50 backdrop-blur-lg rounded-2xl border border-gray-800 p-12 text-center">
              <Clock className="w-16 h-16 mx-auto mb-4 text-gray-600" />
              <p className="text-gray-400 text-lg">No tasks found. Add your first task to get started!</p>
            </div>
          ) : (
            filteredTasks.map((task) => (
              <div
                key={task.id}
                className="bg-gray-900/50 backdrop-blur-lg rounded-xl border border-gray-800 p-6 hover:border-gray-700 transition-all group"
              >
                <div className="flex items-start gap-4">
                  <button
                    onClick={() => toggleTaskStatus(task.id)}
                    className={`mt-1 p-2 rounded-lg border-2 transition-all ${
                      task.status === "completed"
                        ? "bg-emerald-500 border-emerald-500"
                        : "border-gray-700 hover:border-blue-500"
                    }`}
                  >
                    {task.status === "completed" && <Check className="w-5 h-5 text-white" />}
                  </button>
                  <div className="flex-1">
                    <h3
                      className={`text-xl font-semibold mb-2 ${
                        task.status === "completed" ? "line-through text-gray-500" : "text-white"
                      }`}
                    >
                      {task.title}
                    </h3>
                    {task.description && (
                      <p className="text-gray-400 mb-3">{task.description}</p>
                    )}
                    <div className="flex flex-wrap gap-2 items-center">
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-medium border ${getPriorityColor(
                          task.priority
                        )}`}
                      >
                        {task.priority.toUpperCase()}
                      </span>
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(
                          task.status
                        )}`}
                      >
                        {task.status.replace("-", " ").toUpperCase()}
                      </span>
                      {task.dueDate && (
                        <span className="px-3 py-1 rounded-full text-xs font-medium bg-blue-500/20 text-blue-400 border border-blue-500/30 flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          {format(new Date(task.dueDate), "MMM dd, yyyy HH:mm")}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => speakText(task.title)}
                      className="p-2 rounded-lg bg-gray-800 hover:bg-gray-700 border border-gray-700 transition-all opacity-0 group-hover:opacity-100"
                      title="Read aloud"
                    >
                      <Volume2 className="w-5 h-5 text-gray-400" />
                    </button>
                    <button
                      onClick={() => deleteTask(task.id)}
                      className="p-2 rounded-lg bg-red-500/20 hover:bg-red-500/30 border border-red-500/30 transition-all"
                      title="Delete task"
                    >
                      <Trash2 className="w-5 h-5 text-red-400" />
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 bg-gray-900/50 backdrop-blur-lg border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-gray-400">
          <p>
            Created by <span className="text-blue-400 font-semibold">Asif Ali AstolixGen</span> for PIAIC Hackathon 2026
          </p>
          <p className="text-sm mt-2">AI-Powered Project Management System</p>
        </div>
      </footer>

      {/* AI Chatbot */}
      <Chatbot onTaskCommand={handleChatbotCommand} />
    </div>
  );
}
