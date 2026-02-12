'use client'

import { useState, useRef, useEffect } from 'react'
import { MessageCircle, X, Send, Loader2, Bot, Paperclip, Trash2 } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export default function Chatbot() {
  const router = useRouter()
  const { user } = useAuth()
  const [isOpen, setIsOpen] = useState(false)
  const [conversationId, setConversationId] = useState<number | null>(null)
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Hi! I\'m your TaskFlow AI assistant. I can help you manage your tasks. Try saying "Add a task to buy groceries" or "What are my tasks?" You can also upload documents using the 📎 button!'
    }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Get user-specific localStorage key
  const getConversationKey = () => {
    return user?.id ? `chatbot_conversation_id_${user.id}` : null
  }

  // Load conversation from localStorage on mount (user-specific)
  useEffect(() => {
    if (!user?.id) return

    const conversationKey = getConversationKey()
    if (!conversationKey) return

    const savedConversationId = localStorage.getItem(conversationKey)
    if (savedConversationId) {
      const convId = parseInt(savedConversationId)
      setConversationId(convId)
      loadConversation(convId)
    }
  }, [user?.id])

  // Clear conversation when user changes
  useEffect(() => {
    if (!user?.id) {
      setConversationId(null)
      setMessages([
        {
          role: 'assistant',
          content: 'Hi! I\'m your TaskFlow AI assistant. I can help you manage your tasks. Try saying "Add a task to buy groceries" or "What are my tasks?" You can also upload documents using the 📎 button!'
        }
      ])
    }
  }, [user?.id])

  const loadConversation = async (convId: number) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const token = localStorage.getItem('token')

      const response = await fetch(`${apiUrl}/api/chat/conversations/${convId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        setMessages(data.messages.map((msg: any) => ({
          role: msg.role,
          content: msg.content
        })))
      }
    } catch (error) {
      console.error('Failed to load conversation:', error)
    }
  }

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return

    const userMessage = input.trim()
    setInput('')

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setIsLoading(true)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const token = localStorage.getItem('token')

      const response = await fetch(`${apiUrl}/api/chat/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          message: userMessage,
          conversation_id: conversationId // Use conversation_id for persistence
        })
      })

      if (!response.ok) {
        throw new Error('Failed to send message')
      }

      const data = await response.json()

      // Save conversation_id for future messages (user-specific)
      if (data.conversation_id && data.conversation_id !== conversationId) {
        setConversationId(data.conversation_id)
        const conversationKey = getConversationKey()
        if (conversationKey) {
          localStorage.setItem(conversationKey, data.conversation_id.toString())
        }
      }

      // Add AI response
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.response
      }])

      // Trigger task update event if chatbot performed a task operation
      const taskOperationKeywords = ['created', 'added', 'updated', 'deleted', 'removed', 'completed', 'marked'];
      const responseText = data.response.toLowerCase();
      const hasTaskOperation = taskOperationKeywords.some(keyword => responseText.includes(keyword));

      if (hasTaskOperation) {
        console.log('Task operation detected in chatbot response, triggering update...');
        window.dispatchEvent(new CustomEvent('chatbot-task-updated'));
      }

    } catch (error) {
      console.error('Chat error:', error)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please make sure you\'re logged in and the AI service is configured.'
      }])
    } finally {
      setIsLoading(false)
    }
  }

  const startNewConversation = () => {
    setConversationId(null)
    const conversationKey = getConversationKey()
    if (conversationKey) {
      localStorage.removeItem(conversationKey)
    }
    setMessages([
      {
        role: 'assistant',
        content: 'Hi! I\'m your TaskFlow AI assistant. I can help you manage your tasks. Try saying "Add a task to buy groceries" or "What are my tasks?" You can also upload documents using the 📎 button!'
      }
    ])
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <>
      {/* Chat Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-4 right-4 md:bottom-6 md:right-6 w-14 h-14 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full shadow-lg hover:shadow-xl transition-all flex items-center justify-center z-50 group"
          aria-label="Open chat"
        >
          <MessageCircle className="w-6 h-6 text-white group-hover:scale-110 transition-transform" />
          <span className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full animate-pulse"></span>
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed inset-x-0 bottom-0 md:bottom-6 md:right-6 md:left-auto w-full md:w-96 h-[80vh] md:h-[600px] bg-gray-900 rounded-t-2xl md:rounded-2xl shadow-2xl z-50 flex flex-col border border-gray-800">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-4 rounded-t-2xl flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-white font-semibold">AI Assistant</h3>
                <p className="text-white/80 text-xs">
                  {conversationId ? `Chat #${conversationId}` : 'New conversation'}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {conversationId && (
                <button
                  onClick={startNewConversation}
                  className="text-white/80 hover:text-white transition-colors"
                  aria-label="New conversation"
                  title="Start new conversation"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              )}
              <button
                onClick={() => setIsOpen(false)}
                className="text-white/80 hover:text-white transition-colors"
                aria-label="Close chat"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-2 ${
                    message.role === 'user'
                      ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
                      : 'bg-gray-800 text-gray-200'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-800 rounded-2xl px-4 py-2 flex items-center gap-2">
                  <Loader2 className="w-4 h-4 animate-spin text-blue-400" />
                  <span className="text-sm text-gray-400">Thinking...</span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t border-gray-800">
            <div className="flex gap-2">
              <button
                onClick={() => router.push('/files')}
                className="bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg px-3 py-2 transition-all flex items-center justify-center"
                aria-label="Upload files"
                title="Upload documents for AI context"
              >
                <Paperclip className="w-5 h-5" />
              </button>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                disabled={isLoading}
                className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 disabled:opacity-50"
              />
              <button
                onClick={sendMessage}
                disabled={isLoading || !input.trim()}
                className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:from-gray-700 disabled:to-gray-700 text-white rounded-lg px-4 py-2 transition-all disabled:cursor-not-allowed flex items-center justify-center"
                aria-label="Send message"
              >
                {isLoading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Send className="w-5 h-5" />
                )}
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2 text-center">
              AI powered by OpenAI • Conversation auto-saved • 📎 Upload docs
            </p>
          </div>
        </div>
      )}
    </>
  )
}
