import { useAutoScroll } from "../../hooks/useAutoScroll";
import MessageItem from "../MessageItem/MessageItem";
import TypingIndicator from "../TypingIndicator/TypingIndicator";
import type { Message } from "../../types";
import styles from "./MessageList.module.css";

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
}

export default function MessageList({
  messages,
  isLoading,
}: MessageListProps) {
  const containerRef = useAutoScroll([messages.length, isLoading], true);

  return (
    <div ref={containerRef} className={styles.container}>
      {messages.length === 0 && (
        <div className={styles.emptyState}>
          <p>Start a conversation by typing a message below.</p>
          <p className={styles.hint}>
            Try asking about our shipping policy, return policy, or support
            hours.
          </p>
        </div>
      )}

      {messages.map((message, index) => (
        <MessageItem key={index} message={message} />
      ))}

      {isLoading && <TypingIndicator />}
    </div>
  );
}
