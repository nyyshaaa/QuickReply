

import styles from "./TypingIndicator.module.css";

export default function TypingIndicator() {
  return (
    <div className={styles.container}>
      <div className={styles.dots}>
        <span></span>
        <span></span>
        <span></span>
      </div>
      <span className={styles.text}>Agent is typing...</span>
    </div>
  );
}

