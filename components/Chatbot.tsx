"use client";

import { useState, useRef, useEffect } from "react";
import {
  MessageCircle,
  X,
  Send,
  Bot,
  User as UserIcon,
  Sparkles,
  Loader2,
} from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

interface ChatbotProps {
  onTaskCommand?: (command: string) => void;
}

export default function Chatbot({ onTaskCommand }: ChatbotProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "Hello! I'm your AI assistant. I can help you manage tasks using natural language. Try commands like:\n\n• 'Add buy groceries tomorrow'\n• 'Show all high priority tasks'\n• 'Mark task as complete'\n• 'Delete completed tasks'\n\nHow can I help you today?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const processCommand = (userInput: string): string => {
    const lowerInput = userInput.toLowerCase();

    // Add task commands
    if (
      lowerInput.includes("add") ||
      lowerInput.includes("create") ||
      lowerInput.includes("new task")
    ) {
      onTaskCommand?.(userInput);
      return `I'll help you add that task! The task has been created. You can see it in your task list above.`;
    }

    // Show tasks commands
    if (
      lowerInput.includes("show") ||
      lowerInput.includes("list") ||
      lowerInput.includes("view")
    ) {
      if (lowerInput.includes("high priority")) {
        return "Showing all high priority tasks. Check your task list with the high priority filter applied.";
      }
      if (lowerInput.includes("completed")) {
        return "Showing all completed tasks. Use the status filter to see completed tasks.";
      }
      return "Here are all your tasks. You can use the filters above to narrow down your view.";
    }

    // Mark complete commands
    if (
      lowerInput.includes("complete") ||
      lowerInput.includes("done") ||
      lowerInput.includes("finish")
    ) {
      return "To mark a task as complete, click the checkbox next to the task in your list above.";
    }

    // Delete commands
    if (lowerInput.includes("delete") || lowerInput.includes("remove")) {
      return "To delete a task, click the trash icon next to the task you want to remove.";
    }

    // Priority commands
    if (lowerInput.includes("priority")) {
      return "You can set task priority when creating a task. Choose from Low, Medium, or High priority levels.";
    }

    // Voice commands
    if (lowerInput.includes("voice") || lowerInput.includes("speak")) {
      return "Use the microphone icon when adding tasks for voice input. Click the speaker icon on any task to hear it read aloud.";
    }

    // Search commands
    if (lowerInput.includes("search") || lowerInput.includes("find")) {
      return "Use the search bar above to find tasks by title or description. You can also filter by priority and status.";
    }

    // Help commands
    if (
      lowerInput.includes("help") ||
      lowerInput.includes("what can you do") ||
      lowerInput.includes("how")
    ) {
      return `I can help you with:\n\n📝 **Task Management**\n• Add new tasks with natural language\n• Set priorities and due dates\n• View and filter tasks\n\n🎯 **Quick Actions**\n• Mark tasks complete\n• Delete tasks\n• Search tasks\n\n🎤 **Voice Features**\n• Voice input for tasks\n• Text-to-speech for task reading\n\nJust tell me what you'd like to do!`;
    }

    // Greeting commands
    if (
      lowerInput.includes("hello") ||
      lowerInput.includes("hi") ||
      lowerInput.includes("hey")
    ) {
      return "Hello! I'm here to help you manage your tasks efficiently. What would you like to do?";
    }

    // Default response
    return "I'm not sure I understand that command. Try asking me to:\n• Add a new task\n• Show your tasks\n• Help with task management\n\nWhat would you like to do?";
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    // Simulate AI processing delay
    await new Promise((resolve) => setTimeout(resolve, 800));

    const response = processCommand(input);

    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: "assistant",
      content: response,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, assistantMessage]);
    setIsTyping(false);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
      {/* Floating Chat Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 p-4 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white rounded-full shadow-2xl shadow-blue-500/50 transition-all hover:scale-110 z-50 flex items-center gap-2 group"
        >
          <MessageCircle className="w-6 h-6" />
          <span className="max-w-0 overflow-hidden group-hover:max-w-xs transition-all duration-300 whitespace-nowrap">
            AI Assistant
          </span>
          <Sparkles className="w-4 h-4 animate-pulse" />
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-96 h-[600px] bg-gray-900 border border-gray-800 rounded-2xl shadow-2xl z-50 flex flex-col overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="p-2 bg-white/20 rounded-lg backdrop-blur-sm">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="font-semibold text-white">AI Assistant</h3>
                <p className="text-xs text-blue-100">Always here to help</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-2 hover:bg-white/20 rounded-lg transition-all"
            >
              <X className="w-5 h-5 text-white" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-950">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${
                  message.role === "user" ? "flex-row-reverse" : "flex-row"
                }`}
              >
                <div
                  className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                    message.role === "user"
                      ? "bg-blue-500"
                      : "bg-gradient-to-br from-purple-500 to-blue-500"
                  }`}
                >
                  {message.role === "user" ? (
                    <UserIcon className="w-5 h-5 text-white" />
                  ) : (
                    <Bot className="w-5 h-5 text-white" />
                  )}
                </div>
                <div
                  className={`flex-1 ${
                    message.role === "user" ? "text-right" : "text-left"
                  }`}
                >
                  <div
                    className={`inline-block max-w-[80%] p-3 rounded-2xl ${
                      message.role === "user"
                        ? "bg-blue-500 text-white rounded-tr-sm"
                        : "bg-gray-800 text-gray-100 rounded-tl-sm border border-gray-700"
                    }`}
                  >
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    {message.timestamp.toLocaleTimeString([], {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </p>
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="flex gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <div className="bg-gray-800 border border-gray-700 p-3 rounded-2xl rounded-tl-sm">
                  <div className="flex gap-1">
                    <Loader2 className="w-4 h-4 text-gray-400 animate-spin" />
                    <span className="text-sm text-gray-400">Typing...</span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 bg-gray-900 border-t border-gray-800">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me anything..."
                className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
              />
              <button
                onClick={handleSend}
                disabled={!input.trim() || isTyping}
                className="p-3 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:from-gray-700 disabled:to-gray-700 text-white rounded-lg transition-all disabled:cursor-not-allowed"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2 text-center">
              Powered by AI • Created by Asif Ali AstolixGen
            </p>
          </div>
        </div>
      )}
    </>
  );
}
