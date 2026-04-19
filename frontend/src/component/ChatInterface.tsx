import React, { useState } from 'react';
import axios from 'axios';
import { Send, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

interface SourceDocument {
  content: string;
  metadata: Record<string, any>;
}

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  sources?: SourceDocument[];
}

const ChatInterface: React.FC<{ vectorStoreReady: boolean }> = ({ vectorStoreReady }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || !vectorStoreReady) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input,
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/api/query', {
        question: input,
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: response.data.answer,
        sources: response.data.sources,
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error: any) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: error.response?.data?.detail || 'Query failed. Please ensure a document is uploaded.',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md flex flex-col h-[600px]">
      <div className="p-4 border-b">
        <h2 className="text-xl font-semibold">Chat with Documents</h2>
        {!vectorStoreReady && (
          <p className="text-sm text-yellow-600 mt-1">
            ⚠️ No vector store found. Please upload a document first.
          </p>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-400 mt-20">
            <p>Ask a question about your uploaded document</p>
            <p className="text-sm mt-2">Example: "What is the refund policy?"</p>
          </div>
        ) : (
          messages.map(msg => (
            <div
              key={msg.id}
              className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-3 ${
                  msg.type === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                <div className="prose prose-sm max-w-none">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
                
                {msg.sources && msg.sources.length > 0 && (
                  <details className="mt-2 text-xs">
                    <summary className="cursor-pointer opacity-70">Sources ({msg.sources.length})</summary>
                    <div className="mt-1 space-y-1">
                      {msg.sources.map((src, idx) => (
                        <div key={idx} className="border-t border-gray-200 mt-1 pt-1">
                          <p className="italic">{src.content.substring(0, 150)}...</p>
                        </div>
                      ))}
                    </div>
                  </details>
                )}
              </div>
            </div>
          ))
        )}
        
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg p-3 flex items-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span className="text-sm">Thinking...</span>
            </div>
          </div>
        )}
      </div>

      <div className="p-4 border-t">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={vectorStoreReady ? "Ask a question..." : "Upload a document first..."}
            disabled={!vectorStoreReady || loading}
            className="flex-1 border rounded-lg p-2 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={2}
          />
          <button
            onClick={sendMessage}
            disabled={!vectorStoreReady || loading || !input.trim()}
            className="bg-blue-600 text-white px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;