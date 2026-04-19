import { useState, useEffect } from 'react';
import axios from 'axios';
import DocumentUploader from './component/DocumentUploader';
import ChatInterface from './component/ChatInterface';
import { Database } from 'lucide-react';

function App() {
  const [vectorStoreReady, setVectorStoreReady] = useState(false);

  const checkVectorStore = async () => {
    try {
      // Simple way to check if vector store exists - try a dummy query
      await axios.post('http://localhost:8000/api/query', { question: 'test' });
      setVectorStoreReady(true);
    } catch (error: any) {
      // If error is about no vector store, set false; other errors mean it exists
      if (error.response?.status === 400 && error.response?.data?.detail?.includes('not found')) {
        setVectorStoreReady(false);
      } else {
        // Other error means vector store exists (e.g., query format error)
        setVectorStoreReady(true);
      }
    }
  };

  useEffect(() => {
    checkVectorStore();
  }, []);

  const handleUploadSuccess = () => {
    setVectorStoreReady(true);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center gap-2">
            <Database className="w-6 h-6 text-blue-600" />
            <h1 className="text-xl font-semibold">RAG Playground</h1>
            <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded ml-2">
              Naive RAG
            </span>
          </div>
          <p className="text-sm text-gray-500 mt-1">
            Upload documents and ask questions — answers grounded in your content
          </p>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1">
            <DocumentUploader onUploadSuccess={handleUploadSuccess} />
          </div>
          <div className="lg:col-span-2">
            <ChatInterface vectorStoreReady={vectorStoreReady} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;