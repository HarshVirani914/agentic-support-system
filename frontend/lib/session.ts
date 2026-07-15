const SESSION_KEY = "agentic-support-thread-id";

export const getOrCreateSessionId = (): string => {
  if (typeof window === "undefined") return "server";

  let sessionId = localStorage.getItem(SESSION_KEY);
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem(SESSION_KEY, sessionId);
  }
  return sessionId;
};

export const resetSessionId = (): string => {
  const sessionId = crypto.randomUUID();
  localStorage.setItem(SESSION_KEY, sessionId);
  return sessionId;
};
