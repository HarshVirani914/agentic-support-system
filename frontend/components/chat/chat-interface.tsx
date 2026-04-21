"use client";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ApiError, sendChatMessage } from "@/lib/api";
import { ChatMessage as ChatMessageType } from "@/lib/types";
import { AlertCircle, Bot, Loader2, Send, Trash2 } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { ChatMessage } from "./chat-message";
import { SiGithub } from "@icons-pack/react-simple-icons";

export const ChatInterface = () => {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleSubmit = async (e: React.SubmitEvent) => {
    e.preventDefault();

    const trimmedInput = input.trim();
    if (!trimmedInput || isLoading) return;

    setInput("");
    setError(null);

    const userMessage: ChatMessageType = {
      role: "user",
      content: trimmedInput,
      timestamp: Date.now(),
    };
    setMessages((prev) => [...prev, userMessage]);

    setIsLoading(true);
    try {
      const response = await sendChatMessage(trimmedInput);

      const assistantMessage: ChatMessageType = {
        role: "assistant",
        content: response.answer,
        sources: response.sources,
        category: response.category,
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("Failed to send message. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const sampleQuestions = [
    "What is your refund policy?",
    "How long does shipping take?",
    "How do I reset my password?",
    "Do you offer subscriptions?",
  ];

  const handleSampleQuestion = (question: string) => {
    setInput(question);
  };

  const handleClearChat = () => {
    setMessages([]);
    setError(null);
    setInput("");
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

      <Card className="flex-1 mb-4 overflow-hidden flex flex-col">
        <ScrollArea className="h-full w-full">
          <div className="p-4 min-h-full">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center px-4">
                <Bot className="h-16 w-16 text-muted-foreground mb-6" />
                <h2 className="text-2xl font-semibold tracking-tight mb-3">
                  Start a conversation
                </h2>
                <p className="text-[15px] text-muted-foreground mb-8 max-w-md">
                  Try asking one of these questions:
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-3xl">
                  {sampleQuestions.map((question, idx) => (
                    <Button
                      key={idx}
                      variant="outline"
                      className="text-left h-auto py-4 px-5 justify-start hover:bg-muted/50"
                      onClick={() => handleSampleQuestion(question)}
                    >
                      <span className="text-[14px] leading-relaxed">
                        {question}
                      </span>
                    </Button>
                  ))}
                </div>
              </div>
            ) : (
              <div className="max-w-4xl mx-auto space-y-4">
                {messages.map((message, idx) => (
                  <ChatMessage key={idx} message={message} />
                ))}
                {isLoading && (
                  <div className="flex items-center gap-3">
                    <Avatar className="h-8 w-8">
                      <AvatarFallback className="bg-primary/10">
                        <Bot className="h-4 w-4" />
                      </AvatarFallback>
                    </Avatar>
                    <Card className="px-4 py-3 bg-muted">
                      <div className="flex items-center gap-2">
                        <Loader2 className="h-4 w-4 animate-spin" />
                        <span className="text-sm text-muted-foreground">
                          Thinking...
                        </span>
                      </div>
                    </Card>
                  </div>
                )}
                <div ref={scrollRef} />
              </div>
            )}
          </div>
        </ScrollArea>
      </Card>

      {error && (
        <Card className="mb-4 p-4 bg-destructive/10 border-destructive">
          <div className="flex items-center gap-2">
            <AlertCircle className="h-4 w-4 text-destructive" />
            <p className="text-sm text-destructive">{error}</p>
          </div>
        </Card>
      )}

      <Card className="p-4">
        <form
          onSubmit={handleSubmit}
          className="flex gap-2 max-w-4xl mx-auto w-full"
        >
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your question here..."
            disabled={isLoading}
            className="flex-1 text-[15px]"
          />
          <Button type="submit" disabled={isLoading || !input.trim()}>
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </form>
      </Card>

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
