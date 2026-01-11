import { apiRequest } from "./api";

/**
 * Response shape from chat-service
 */
export type ChatResponse = {
  reply: string;
  persona: string;
};

/**
 * Send a chat message to the backend
 *
 * Backend:
 * POST http://localhost:8000/chat?message=...&persona=...
 *
 * Auth:
 * Authorization: Bearer <JWT>
 */
export async function sendChatMessage(
  message: string,
  persona: string = "goku"
): Promise<ChatResponse> {
  if (!message.trim()) {
    throw new Error("Message cannot be empty");
  }

  return apiRequest<ChatResponse>(
    "chat",
    `/chat?message=${encodeURIComponent(message)}&persona=${persona}`,
    {
      method: "POST",
    }
  );
}