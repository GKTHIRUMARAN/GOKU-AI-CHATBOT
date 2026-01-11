"use client";

import { usePathname, useRouter } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();

  const isChatActive = pathname.startsWith("/chat");

  return (
    <aside className="flex h-full w-64 flex-col border-r border-border bg-background">
      {/* Header */}
      <div className="flex h-14 items-center border-b border-border px-4">
        <span className="text-lg font-semibold tracking-tight">
          Goku AI
        </span>
      </div>

      {/* Navigation */}
      <nav className="flex flex-1 flex-col p-2">
        <button
          onClick={() => router.push("/chat")}
          className={`flex items-center rounded-md px-3 py-2 text-sm font-medium transition
            ${
              isChatActive
                ? "bg-primary text-primary-foreground"
                : "text-muted hover:bg-muted/20"
            }`}
        >
          💬 Chat
        </button>

        {/* Divider */}
        <div className="my-3 border-t border-border" />

        {/* Placeholder: Conversations */}
        <div className="px-3 text-xs font-semibold uppercase tracking-wide text-muted">
          Conversations
        </div>

        <div className="mt-2 space-y-1 px-1 text-sm text-muted">
          <div className="rounded-md px-3 py-2 italic opacity-70">
            Coming soon
          </div>
        </div>
      </nav>

      {/* Footer */}
      <div className="border-t border-border px-4 py-3 text-xs text-muted">
        v1.0 • Goku AI
      </div>
    </aside>
  );
}