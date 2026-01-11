import { apiRequest } from "./api";
import { storage } from "./storage";

/**
 * Expected response from auth service
 */
export type AuthResponse = {
  access_token: string;
  token_type: string;
};

/**
 * Signup a new user
 * - Does NOT auto-login
 * - Redirect handled by page
 */
export async function signup(
  email: string,
  password: string
): Promise<void> {
  await apiRequest(
    "auth",
    "/auth/signup",
    {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }
  );
}

/**
 * Login user
 * - Stores JWT token
 * - Must complete BEFORE redirect
 */
export async function login(
  email: string,
  password: string
): Promise<AuthResponse> {
  const res = await apiRequest<AuthResponse>(
    "auth",
    "/auth/login",
    {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }
  );

  // 🔑 Critical: persist token
  storage.setToken(res.access_token);

  return res;
}

/**
 * Logout user
 * - Clears token only
 */
export function logout(): void {
  storage.clear();
}

/**
 * Auth state check
 * - Used by route guards
 */
export function isAuthenticated(): boolean {
  return !!storage.getToken();
}