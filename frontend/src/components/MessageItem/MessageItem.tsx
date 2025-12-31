import type { Message } from "../../types";
import styles from "./MessageItem.module.css";

interface MessageItemProps {
  message: Message;
}

export default function MessageItem({ message }: MessageItemProps) {
  const isUser = message.sender === "user";
  const isSystem = message.sender === "system";

  return (
    <div
      className={`${styles.message} ${
        isUser
          ? styles.userMessage
          : isSystem
          ? styles.systemMessage
          : styles.aiMessage
      }`}
    >
      <div className={styles.text}>{message.text}</div>
    </div>
  );
}

