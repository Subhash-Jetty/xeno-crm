export interface User {
  name: string;
  email: string;
  company: string;
}

const STORAGE_KEY = "xeno_user";

export function getUser(): User | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function login(user: User): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(user));
}

export function logout(): void {
  localStorage.removeItem(STORAGE_KEY);
  window.location.href = "/login";
}

export function isAuthenticated(): boolean {
  return getUser() !== null;
}

export function getGreeting(): string {
  const hour = new Date().getHours();
  if (hour < 12) return "Good morning";
  if (hour < 17) return "Good afternoon";
  return "Good evening";
}
