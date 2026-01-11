"use client";

import { useRouter } from "next/navigation";
import { storage } from "@/lib/storage";

export default function TopBar() {
  const router = useRouter();

  function logout() {
    storage.clearToken();
    router.replace("/login"); // replace prevents back-navigation
  }

  return (
    <header className="flex items-center justify-between px-6 py-4 border-b border-border">
      <h1 className="text-lg font-semibold">Goku AI</h1>

      <button
        onClick={logout}
        className="text-sm text-muted-foreground hover:text-foreground"
      >
        Logout
      </button>
    </header>
  );
}