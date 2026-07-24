// Central token storage. Version 1 stores the access token in localStorage; the
// refresh token is also held by an HttpOnly cookie set by the backend, so the
// localStorage copy is a convenience for the SPA and can be revoked by logout.

const ACCESS_KEY = "aci.access_token";
const REFRESH_KEY = "aci.refresh_token";

export const tokenStore = {
  getAccessToken(): string | null {
    return localStorage.getItem(ACCESS_KEY);
  },
  setAccessToken(token: string): void {
    localStorage.setItem(ACCESS_KEY, token);
  },
  getRefreshToken(): string | null {
    return localStorage.getItem(REFRESH_KEY);
  },
  setRefreshToken(token: string): void {
    localStorage.setItem(REFRESH_KEY, token);
  },
  setTokens(access: string, refresh: string): void {
    localStorage.setItem(ACCESS_KEY, access);
    localStorage.setItem(REFRESH_KEY, refresh);
  },
  clear(): void {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
  },
};
