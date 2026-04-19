import React, { useState } from 'react';
import axios from 'axios';
import { Upload, FileText, CheckCircle, XCircle } from 'lucide-react';

interface IngestResponse {
  message: string;
  num_chunks: number;
  persisted_path: string;
}

interface DocumentUploaderProps {
  onUploadSuccess: () => void;
}

const DocumentUploader: React.FC<DocumentUploaderProps> = ({ onUploadSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState<{ type: 'success' | 'error' | null; message: string }>({ type: null, message: '' });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setStatus({ type: null, message: '' });
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setStatus({ type: 'error', message: 'Please select a file first' });
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post<IngestResponse>('http://localhost:8000/api/ingest', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setStatus({ type: 'success', message: `Success! ${response.data.num_chunks} chunks indexed.` });
      setFile(null);
      onUploadSuccess();
      
      // Reset file input
      const fileInput = document.getElementById('file-input') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
    } catch (error: any) {
      setStatus({ type: 'error', message: error.response?.data?.detail || 'Upload failed' });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
        <FileText className="w-5 h-5" />
        Document Upload
      </h2>
      
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
        <input
          id="file-input"
          type="file"
          accept=".txt,.pdf"
          onChange={handleFileChange}
          className="hidden"
        />
        <label
          htmlFor="file-input"
          className="cursor-pointer inline-flex flex-col items-center gap-2"
        >
          <Upload className="w-10 h-10 text-gray-400" />
          <span className="text-sm text-gray-600">
            {file ? file.name : 'Click to select PDF or TXT'}
          </span>
        </label>
      </div>

      {file && (
        <button
          onClick={handleUpload}
          disabled={uploading}
          className="mt-4 w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:bg-blue-300 transition-colors"
        >
          {uploading ? 'Uploading...' : 'Upload Document'}
        </button>
      )}

      {status.type && (
        <div className={`mt-4 p-3 rounded-lg flex items-center gap-2 ${
          status.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
        }`}>
          {status.type === 'success' ? <CheckCircle className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
          {status.message}
        </div>
      )}
    </div>
  );
};

export default DocumentUploader;