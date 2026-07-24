import axios, { AxiosError, type AxiosInstance } from "axios";
import type { ErrorEnvelope, SuccessEnvelope } from "@/types/api";
import { tokenStore } from "@/services/tokenStore";

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

/** A normalised API error carrying the backend error code + message. */
export class ApiError extends Error {
  code: string;
  status: number;
  details?: { field: string; message: string }[];

  constructor(message: string, code: string, status: number, details?: ErrorEnvelope["error"]["details"]) {
    super(message);
    this.name = "ApiError";
    this.code = code;
    this.status = status;
    this.details = details;
  }
}

const client: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
});

// Attach the access token to every request.
client.interceptors.request.use((config) => {
  const token = tokenStore.getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

let refreshing: Promise<string | null> | null = null;

async function refreshAccessToken(): Promise<string | null> {
  const refreshToken = tokenStore.getRefreshToken();
  if (!refreshToken) return null;
  try {
    const resp = await axios.post<SuccessEnvelope<{ access_token: string; expires_in: number }>>(
      `${BASE_URL}/auth/refresh`,
      { refresh_token: refreshToken },
      { withCredentials: true },
    );
    const newToken = resp.data.data.access_token;
    tokenStore.setAccessToken(newToken);
    return newToken;
  } catch {
    tokenStore.clear();
    return null;
  }
}

// Transparently refresh the access token once on 401, then retry.
client.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<ErrorEnvelope>) => {
    const original = error.config;
    const status = error.response?.status ?? 0;
    const code = error.response?.data?.error?.code;

    if (status === 401 && code !== "OAUTH_FAILED" && original && !(original as { _retried?: boolean })._retried) {
      (original as { _retried?: boolean })._retried = true;
      refreshing = refreshing ?? refreshAccessToken();
      const newToken = await refreshing;
      refreshing = null;
      if (newToken) {
        original.headers = original.headers ?? {};
        original.headers.Authorization = `Bearer ${newToken}`;
        return client(original);
      }
    }

    const body = error.response?.data;
    throw new ApiError(
      body?.error?.message ?? error.message ?? "Request failed.",
      body?.error?.code ?? "NETWORK_ERROR",
      status,
      body?.error?.details,
    );
  },
);

/** Unwrap the backend success envelope and return the inner data. */
export async function unwrap<T>(promise: Promise<{ data: SuccessEnvelope<T> }>): Promise<T> {
  const response = await promise;
  return response.data.data;
}

export default client;
