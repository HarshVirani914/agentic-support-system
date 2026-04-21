import { ChatRequest, ChatResponse, ChatError } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public details?: ChatError
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export const sendChatMessage = async (
  message: string,
  limit: number = 3
): Promise<ChatResponse> => {
  const body: ChatRequest = {
    message,
    limit,
  };

  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      let errorDetails: ChatError | undefined;
      try {
        errorDetails = await response.json();
      } catch {
      }

      throw new ApiError(
        errorDetails?.message || `Request failed with status ${response.status}`,
        response.status,
        errorDetails
      );
    }

    const data: ChatResponse = await response.json();
    return data;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }

    throw new ApiError(
      error instanceof Error ? error.message : "An unexpected error occurred"
    );
  }
};

export const checkApiHealth = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
};
