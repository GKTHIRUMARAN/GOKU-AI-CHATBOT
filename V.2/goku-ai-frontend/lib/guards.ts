"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { storage } from "./storage";

export function useRequireAuth() {
  const router = useRouter();

  useEffect(() => {
    const token = storage.getToken();
    if (!token) {
      router.replace("/login");
    }
  }, [router]);
}