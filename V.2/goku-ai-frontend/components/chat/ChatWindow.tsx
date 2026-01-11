"use client";

import { useState } from "react";
import MessageBubble from "./MessageBubble";
import ChatInput from "./ChatInput";

type Message = {
  role: "user" | "assistant";
  content: string;
};

interface Props {
  messages: Message[];
  onSend: (text: string) => void;
  loading?: boolean;
}

export default function ChatWindow({ messages, onSend, loading }: Props) {
  return (
    <div className="flex flex-1 justify-center overflow-hidden">
      {/* CENTER COLUMN */}
      <div className="flex flex-col w-full max-w-3xl h-full">
        {/* MESSAGES */}
        <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
          {messages.length === 0 && (
            <div className="text-muted-foreground text-center mt-20">
              Start a conversation with Goku.
            </div>
          )}

          {messages.map((msg, i) => (
            <MessageBubble
              key={i}
              role={msg.role}
              content={msg.content}
            />
          ))}
        </div>

        {/* INPUT */}
        <div className="border-t border-border px-4 py-3">
          <ChatInput onSend={onSend} disabled={loading} />
        </div>
      </div>
    </div>
  );
}