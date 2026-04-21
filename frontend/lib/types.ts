export interface Source {
  text: string;
  score: number;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  category?: string;
  timestamp: number;
}

export interface ChatRequest {
  message: string;
  limit?: number;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
  category: string;
}

export interface ChatError {
  error: string;
  message: string;
  path?: string;
}
