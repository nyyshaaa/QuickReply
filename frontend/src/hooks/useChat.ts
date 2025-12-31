import { useCallback, useState } from "react";
import { sendChatMessage } from "../api/chat";


export type ChatSender = "user" | "ai" | "system";

import { uuidv7 } from "uuidv7";

export function generateSessionId(): string {
  return uuidv7();
}

export interface ChatMessage {
  sender: ChatSender;
  text: string;
}

export function useChat() {
  const [sessionId, setSessionId] = useState<string>(() =>
    generateSessionId()
  );

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (text: string) => {
      if (!text.trim() || isLoading) return;

      setIsLoading(true);
      setError(null);

      setMessages((prev) => [
        ...prev,
        { sender: "user", text },
      ]);

      try {
        const { reply, session_id } = await sendChatMessage(
          text,
          sessionId
        );

        setSessionId(session_id);

        setMessages((prev) => [
          ...prev,
          { sender: "ai", text: reply },
        ]);
      } catch (err: any) {
        const message =
          err?.message ?? "Something went wrong. Please try again.";

        setMessages((prev) => [
          ...prev,
          { sender: "system", text: message },
        ]);

        setError(message);
      } finally {
        setIsLoading(false);
      }
    },
    [sessionId, isLoading]
  );

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearError: () => setError(null),
  };
}
