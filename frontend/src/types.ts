

export type Sender = "user" | "ai" | "system";

export interface Message {
  sender: Sender;
  text: string;
  timestamp?: Date;
}

export interface ChatState {
  messages: Message[];
  sessionId: string;
  isLoading: boolean;
  error: string | null;
}
