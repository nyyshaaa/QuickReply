
import { useChat } from "../../hooks/useChat";
import MessageInput from "../MessageInput/MessageInput";
import ErrorMessage from "../ErrorMessage/ErrorMessage";
import styles from "./ChatWidget.module.css";
import MessageList from "../MessageList/MessageList";

export default function ChatWidget() {
  const { messages, isLoading, error, sendMessage, clearError } = useChat();

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2 className={styles.title}>AI Support Agent</h2>
        <p className={styles.subtitle}>How can we help you today?</p>
      </div>

      <MessageList messages={messages} isLoading={isLoading} />

      {error && <ErrorMessage message={error} onDismiss={clearError} />}

      <MessageInput onSend={sendMessage} disabled={isLoading} />
    </div>
  );
}

