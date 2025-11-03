import { Brain, Eraser, Settings } from "lucide-react";
import useChatStore from "../store/chatStore";

export default function HeaderBar() {
  const clearChat = useChatStore((s) => s.clearChat);

  return (
    <header className="flex items-center justify-between px-4 py-3 border-b border-slate-800 bg-slate-900/50">
      <h1 className="text-xl font-semibold text-orange-400">
        🔥 Project Z — Goku AI
      </h1>
      <div className="flex gap-4 text-slate-300">
        <button
          onClick={clearChat}
          title="Clear Chat"
          className="hover:text-orange-400"
        >
          <Eraser size={20} />
        </button>
        <button title="Memory (coming soon)" className="hover:text-orange-400">
          <Brain size={20} />
        </button>
        <button title="Settings (coming soon)" className="hover:text-orange-400">
          <Settings size={20} />
        </button>
      </div>
    </header>
  );
}
