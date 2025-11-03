import { useEffect, useRef } from "react";
import useChatStore from "../store/chatStore";
import ChatMessage from "../components/ChatMessage";
import ChatInput from "../components/ChatInput";

export default function ChatPage() {
  const messages = useChatStore((s) => s.messages);
  const bottomRef = useRef();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((m, i) => (
          <ChatMessage key={i} role={m.role} text={m.text} />
        ))}
        <div ref={bottomRef} />
      </div>
      <ChatInput />
    </div>
  );
}
