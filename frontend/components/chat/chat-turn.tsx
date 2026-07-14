"use client";

import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Message, MessageAvatar, MessageContent } from "@/components/ui/message";
import {
  Reasoning,
  ReasoningContent,
  ReasoningTrigger,
} from "@/components/ai-elements/reasoning";
import { Shimmer } from "@/components/ai-elements/shimmer";
import {
  Sources,
  SourcesContent,
  SourcesTrigger,
} from "@/components/ai-elements/sources";
import { ChatMessage as ChatMessageType } from "@/lib/types";
import { cn } from "@/lib/utils";
import { Bot, User } from "lucide-react";

interface ChatTurnProps {
  message: ChatMessageType;
}

const getCategoryColor = (category?: string) => {
  switch (category) {
    case "order":
      return "bg-blue-500 hover:bg-blue-600";
    case "shipping":
      return "bg-green-500 hover:bg-green-600";
    default:
      return "bg-gray-500 hover:bg-gray-600";
  }
};

export const ChatTurn = ({ message }: ChatTurnProps) => {
  const isUser = message.role === "user";

  return (
    <Message align={isUser ? "end" : "start"} className="mb-4">
      <MessageAvatar>
        {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
      </MessageAvatar>
      <MessageContent
        className={cn(
          "rounded-lg px-4 py-3 max-w-[80%]",
          isUser ? "bg-primary text-primary-foreground" : "bg-muted"
        )}
      >
        <p className="text-[15px] leading-relaxed whitespace-pre-wrap">
          {message.content}
        </p>

        {!isUser && message.category && (
          <div className="flex items-center gap-2">
            <Badge className={cn("text-xs", getCategoryColor(message.category))}>
              {message.category.charAt(0).toUpperCase() +
                message.category.slice(1)}{" "}
              Query
            </Badge>
            {message.retryCount !== undefined && message.retryCount > 0 && (
              <Badge variant="outline" className="text-xs">
                Re-checked {message.retryCount}x
              </Badge>
            )}
          </div>
        )}

        {!isUser && message.gradingReason && (
          <Reasoning isStreaming={false} defaultOpen={false}>
            <ReasoningTrigger>
              <span className="text-xs font-semibold uppercase tracking-wide">
                {message.grounded ? "Grounding check" : "Grounding check (low confidence)"}
              </span>
            </ReasoningTrigger>
            <ReasoningContent>
              {message.grounded
                ? `Grounded in retrieved sources: ${message.gradingReason}`
                : `Answered with lower confidence after ${message.retryCount ?? 0} retries: ${message.gradingReason}`}
            </ReasoningContent>
          </Reasoning>
        )}

        {!isUser && message.sources && message.sources.length > 0 && (
          <Sources>
            <SourcesTrigger count={message.sources.length} />
            <SourcesContent>
              {message.sources.map((source, idx) => (
                <Card key={idx} className="w-72 max-w-full p-3 bg-muted/50">
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <p className="text-xs font-semibold">Source {idx + 1}</p>
                    <Badge variant="outline" className="text-xs">
                      {(source.score * 100).toFixed(1)}% relevant
                    </Badge>
                  </div>
                  <p className="text-[13px] leading-relaxed text-muted-foreground line-clamp-3">
                    {source.text}
                  </p>
                </Card>
              ))}
            </SourcesContent>
          </Sources>
        )}
      </MessageContent>
    </Message>
  );
};

ChatTurn.Thinking = function Thinking() {
  return (
    <Message align="start" className="mb-4">
      <MessageAvatar>
        <Bot className="h-4 w-4" />
      </MessageAvatar>
      <MessageContent className="rounded-lg px-4 py-3 bg-muted">
        <Shimmer className="text-sm" duration={1.5}>
          Searching knowledge base…
        </Shimmer>
      </MessageContent>
    </Message>
  );
};
