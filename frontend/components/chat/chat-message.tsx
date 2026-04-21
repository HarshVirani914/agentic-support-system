import { ChatMessage as ChatMessageType } from "@/lib/types";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { Bot, User, Copy, Check, ChevronDown, ChevronUp } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage = ({ message }: ChatMessageProps) => {
  const [copied, setCopied] = useState(false);
  const [sourcesOpen, setSourcesOpen] = useState(false);
  const isUser = message.role === "user";

  const handleCopy = async () => {
    await navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getCategoryColor = (category?: string) => {
    switch (category) {
      case "order":
        return "bg-blue-500 hover:bg-blue-600";
      case "shipping":
        return "bg-green-500 hover:bg-green-600";
      case "general":
        return "bg-gray-500 hover:bg-gray-600";
      default:
        return "bg-gray-500 hover:bg-gray-600";
    }
  };

  const formatTimestamp = (timestamp: number) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString("en-US", {
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    });
  };

  return (
    <div
      className={cn(
        "flex gap-3 mb-4",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      {!isUser && (
        <Avatar className="h-8 w-8 mt-1">
          <AvatarFallback className="bg-primary/10">
            <Bot className="h-4 w-4" />
          </AvatarFallback>
        </Avatar>
      )}

      <div className={cn("flex flex-col gap-2", isUser ? "items-end" : "items-start", "max-w-[80%]")}>
        <Card
          className={cn(
            "px-4 py-3",
            isUser
              ? "bg-primary text-primary-foreground"
              : "bg-muted"
          )}
        >
          <div className="flex items-start justify-between gap-2">
            <p className="text-[15px] leading-relaxed whitespace-pre-wrap">{message.content}</p>
            {!isUser && (
              <button
                onClick={handleCopy}
                className="text-muted-foreground hover:text-foreground transition-colors"
                title="Copy message"
              >
                {copied ? (
                  <Check className="h-4 w-4" />
                ) : (
                  <Copy className="h-4 w-4" />
                )}
              </button>
            )}
          </div>
        </Card>

        <div className="flex items-center gap-2 px-1">
          <span className="text-xs text-muted-foreground">
            {formatTimestamp(message.timestamp)}
          </span>
          {!isUser && message.category && (
            <Badge className={cn("text-xs", getCategoryColor(message.category))}>
              {message.category.charAt(0).toUpperCase() + message.category.slice(1)} Query
            </Badge>
          )}
        </div>

        {!isUser && message.sources && message.sources.length > 0 && (
          <Collapsible open={sourcesOpen} onOpenChange={setSourcesOpen} className="w-full">
            <CollapsibleTrigger className="flex items-center gap-2 text-xs font-semibold text-muted-foreground uppercase tracking-wide hover:text-foreground transition-colors">
              {sourcesOpen ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
              {sourcesOpen ? "Hide" : "Show"} Sources ({message.sources.length})
            </CollapsibleTrigger>
            <CollapsibleContent className="space-y-2 mt-2">
              {message.sources.map((source, idx) => (
                <Card key={idx} className="p-3 bg-muted/50">
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
            </CollapsibleContent>
          </Collapsible>
        )}
      </div>

      {isUser && (
        <Avatar className="h-8 w-8 mt-1">
          <AvatarFallback className="bg-primary">
            <User className="h-4 w-4 text-primary-foreground" />
          </AvatarFallback>
        </Avatar>
      )}
    </div>
  );
};
