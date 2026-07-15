export interface Source {
  text: string;
  score: number;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  category?: string;
  retryCount?: number;
  grounded?: boolean;
  gradingReason?: string;
  timestamp: number;
}

export interface ChatRequest {
  message: string;
  limit?: number;
  thread_id: string;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
  category: string;
  retry_count: number;
  grounded: boolean;
  grading_reason: string;
}

export interface ChatError {
  error: string;
  message: string;
  path?: string;
}
