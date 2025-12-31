
import styles from "./ErrorMessage.module.css";

interface ErrorMessageProps {
  message: string;
  onDismiss: () => void;
}

export default function ErrorMessage({ message, onDismiss }: ErrorMessageProps) {
  return (
    <div className={styles.container} role="alert">
      <span className={styles.icon}>⚠️</span>
      <span className={styles.text}>{message}</span>
      <button
        className={styles.dismissButton}
        onClick={onDismiss}
        aria-label="Dismiss error"
      >
        ×
      </button>
    </div>
  );
}

