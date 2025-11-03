import { useState } from "react";
import useChatStore from "../store/chatStore";

export default function ChatInput() {
  const [input, setInput] = useState("");
  const sendMessage = useChatStore((s) => s.sendMessage);
  const loading = useChatStore((s) => s.loading);

  const handleSend = async () => {
    if (!input.trim()) return;
    await sendMessage(input.trim());
    setInput("");
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex items-center gap-2 border-t border-slate-800 bg-slate-900/70 p-3">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKey}
        placeholder="Type your message..."
        rows={1}
        className="flex-1 resize-none rounded-xl bg-slate-800 text-slate-100 p-2 text-sm focus:outline-none"
      />
      <button
        onClick={handleSend}
        disabled={loading}
        className="rounded-xl bg-orange-500 px-4 py-2 text-sm font-semibold text-slate-900 hover:bg-orange-400 disabled:opacity-50"
      >
        {loading ? "..." : "Send ⚡"}
      </button>
    </div>
  );
}
