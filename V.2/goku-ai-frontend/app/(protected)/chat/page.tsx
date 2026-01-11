"use client";

import { useState } from "react";
import ChatWindow from "@/components/chat/ChatWindow";
import { sendChatMessage } from "@/lib/chat";

export type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleSend(message: string) {
    if (!message.trim() || loading) return;

    // 1️⃣ Add user message immediately
    setMessages((prev) => [
      ...prev,
      { role: "user", content: message },
    ]);

    setLoading(true);

    try {
      // 2️⃣ Call backend chat service
      const res = await sendChatMessage(message);

      // 3️⃣ Append assistant reply
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.reply },
      ]);
    } catch (err) {
      // 4️⃣ Graceful failure message
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "⚠️ Goku is having trouble responding right now.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-full">
      <ChatWindow
        messages={messages}
        onSend={handleSend}
        loading={loading}
      />
    </div>
  );
}