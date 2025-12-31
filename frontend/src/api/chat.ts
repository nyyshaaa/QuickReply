
export interface ChatMessageRequest {
  message: string;
  session_id: string;
}

export interface ChatMessageResponse {
  session_id: string;
  reply: string;
}

if (!import.meta.env.VITE_API_BASE_URL) {
  throw new Error("VITE_API_BASE_URL is not defined");
}
const API_URL = import.meta.env.VITE_API_BASE_URL;

const CHAT_ENDPOINT = `${API_URL}/chat/message`;

const MAX_MESSAGE_LENGTH = 1500;


export async function sendChatMessage(
  message: string,
  sessionId: string
): Promise<ChatMessageResponse> {
  // ---- Basic client-side validation ----
  const trimmedMessage = message.trim();

  if (!trimmedMessage) {
    throw new Error("Message cannot be empty");
  }

  if (trimmedMessage.length > MAX_MESSAGE_LENGTH) {
    throw new Error(
      `Message is too long. Please keep it under ${MAX_MESSAGE_LENGTH} characters.`
    );
  }

  if (!sessionId) {
    throw new Error("Session ID is required");
  }

  // ---- API call ----
  let response: Response;

  try {
    response = await fetch(CHAT_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: trimmedMessage,
        session_id: sessionId,
      } satisfies ChatMessageRequest),
    });
  } catch {
    // Network / CORS / DNS failure
    throw new Error("Network error. Please check your connection.");
  }

  // ---- HTTP-level errors ----
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      errorText || "Failed to send message. Please try again."
    );
  }

  // ---- Parse & validate response ----
  const data = (await response.json()) as Partial<ChatMessageResponse>;

  if (!data.reply || !data.session_id) {
    throw new Error("Invalid response received from server");
  }

  return {
    reply: data.reply,
    session_id: data.session_id,
  };
}


