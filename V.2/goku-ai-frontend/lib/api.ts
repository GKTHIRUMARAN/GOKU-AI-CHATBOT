import { storage } from "./storage";

/**
 * Backend base URLs
 * (explicit ports — DO NOT inline elsewhere)
 */
const AUTH_BASE = "http://localhost:8001";
const CHAT_BASE = "http://localhost:8000";

/**
 * Generic API request helper
 * - Attaches JWT automatically
 * - Handles JSON
 * - Throws readable errors
 */
export async function apiRequest<T = any>(
  base: "auth" | "chat",
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = storage.getToken();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const BASE_URL = base === "auth" ? AUTH_BASE : CHAT_BASE;

  const response = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let message = "Request failed";
    try {
      const data = await response.json();
      message = data.detail || data.message || message;
    } catch {
      message = await response.text();
    }
    throw new Error(message);
  }

  return response.json();
}