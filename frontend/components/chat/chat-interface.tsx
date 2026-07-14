"use client";

import { Button } from "@/components/ui/button";
import {
  Conversation,
  ConversationContent,
  ConversationEmptyState,
  ConversationScrollButton,
} from "@/components/ai-elements/conversation";
import {
  PromptInput,
  PromptInputTextarea,
  PromptInputSubmit,
  type PromptInputMessage,
} from "@/components/ai-elements/prompt-input";
import { Suggestion, Suggestions } from "@/components/ai-elements/suggestion";
import { ApiError, clearThread, sendChatMessage } from "@/lib/api";
import { getOrCreateSessionId, resetSessionId } from "@/lib/session";
import { ChatMessage as ChatMessageType } from "@/lib/types";
import { AlertCircle, Bot, Trash2 } from "lucide-react";
import { useState } from "react";
import { SiGithub } from "@icons-pack/react-simple-icons";
import { ChatTurn } from "./chat-turn";

const SAMPLE_QUESTIONS = [
  "What is your refund policy?",
  "How long does shipping take?",
  "How do I reset my password?",
  "Do you offer subscriptions?",
];

export const ChatInterface = () => {
  // Lazy initializer runs once on mount; on the client it reads/creates the
  // persisted session id from localStorage. threadId is never rendered into
  // the DOM, so the server/client value mismatch during the initial render
  // is inconsequential (no hydration warning risk).
  const [threadId, setThreadId] = useState<string>(() =>
    getOrCreateSessionId()
  );
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSend = async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;

    setError(null);
    setMessages((prev) => [
      ...prev,
      { role: "user", content: trimmed, timestamp: Date.now() },
    ]);
    setIsLoading(true);

    try {
      const response = await sendChatMessage(trimmed, threadId);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: response.answer,
          sources: response.sources,
          category: response.category,
          retryCount: response.retry_count,
          grounded: response.grounded,
          gradingReason: response.grading_reason,
          timestamp: Date.now(),
        },
      ]);
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.message
          : "Failed to send message. Please try again."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handlePromptSubmit = (message: PromptInputMessage) => {
    return handleSend(message.text ?? "");
  };

  const handleClearChat = async () => {
    await clearThread(threadId);
    setThreadId(resetSessionId());
    setMessages([]);
    setError(null);
  };

  return (
    <div className="flex flex-col h-screen w-full max-w-5xl mx-auto p-4">
      <div className="mb-6 flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight mb-1">
            AI Customer Support
          </h1>
          <p className="text-[15px] text-muted-foreground">
            Ask me anything about our products and services
          </p>
        </div>
        {messages.length > 0 && (
          <Button
            variant="outline"
            size="sm"
            onClick={handleClearChat}
            className="flex items-center gap-2"
          >
            <Trash2 className="h-4 w-4" />
            Clear Chat
          </Button>
        )}
      </div>

      <Conversation className="flex-1 mb-4">
        <ConversationContent>
          {messages.length === 0 ? (
            <ConversationEmptyState>
              <Bot className="h-10 w-10 text-muted-foreground" />
              <div className="space-y-1">
                <h3 className="font-medium text-sm">Start a conversation</h3>
                <p className="text-muted-foreground text-sm">
                  Try asking one of these questions
                </p>
              </div>
              <Suggestions>
                {SAMPLE_QUESTIONS.map((question) => (
                  <Suggestion
                    key={question}
                    suggestion={question}
                    onClick={handleSend}
                  />
                ))}
              </Suggestions>
            </ConversationEmptyState>
          ) : (
            messages.map((message, idx) => (
              <ChatTurn key={idx} message={message} />
            ))
          )}
          {isLoading && <ChatTurn.Thinking />}
        </ConversationContent>
        <ConversationScrollButton />
      </Conversation>

      {error && (
        <div className="mb-4 p-4 rounded-md bg-destructive/10 border border-destructive flex items-center gap-2">
          <AlertCircle className="h-4 w-4 text-destructive" />
          <p className="text-sm text-destructive">{error}</p>
        </div>
      )}

      <PromptInput onSubmit={handlePromptSubmit}>
        <PromptInputTextarea
          placeholder="Type your question here..."
          disabled={isLoading}
        />
        <PromptInputSubmit
          disabled={isLoading}
          status={isLoading ? "streaming" : undefined}
        />
      </PromptInput>

      <div className="flex items-center justify-center gap-4 mt-4 text-sm text-muted-foreground">
        <span>Powered by LangGraph</span>
        <span>•</span>
        <a
          href="https://github.com/HarshVirani914/agentic-support-system"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1 hover:text-foreground transition-colors"
        >
          <SiGithub className="h-4 w-4" />
          View on GitHub
        </a>
      </div>
    </div>
  );
};
