export interface SourceDocument {
  content: string;
  metadata: Record<string, any>;
}

export interface QueryResponse {
  answer: string;
  sources: SourceDocument[];
}

export interface IngestResponse {
  message: string;
  num_chunks: number;
  persisted_path: string;
}