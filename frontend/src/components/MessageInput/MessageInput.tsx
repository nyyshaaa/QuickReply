

import { useState, useCallback, KeyboardEvent, useRef, useEffect } from "react";
import styles from "./MessageInput.module.css";

interface MessageInputProps {
  onSend: (message: string) => void;
  disabled: boolean;
  maxLength?: number;
}

const DEFAULT_MAX_LENGTH = 1500;

export default function MessageInput({
  onSend,
  disabled,
  maxLength = DEFAULT_MAX_LENGTH,
}: MessageInputProps) {
  const [value, setValue] = useState("");
  const [charCount, setCharCount] = useState(0);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
    }
  }, [value]);

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLTextAreaElement>) => {
      const newValue = e.target.value;
      if (newValue.length <= maxLength) {
        setValue(newValue);
        setCharCount(newValue.length);
      }
    },
    [maxLength]
  );

  const handleSend = useCallback(() => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;

    onSend(trimmed);
    setValue("");
    setCharCount(0);
  }, [value, disabled, onSend]);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    },
    [handleSend]
  );

  const isNearLimit = charCount > maxLength * 0.9;
  const isAtLimit = charCount >= maxLength;

  return (
    <div className={styles.container}>
      <div className={styles.inputWrapper}>
        <textarea
          ref={textareaRef}
          className={styles.input}
          value={value}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder="Type your message... (Press Enter to send, Shift+Enter for new line)"
          disabled={disabled}
          rows={1}
        />
        {charCount > 0 && (
          <div
            className={`${styles.charCount} ${
              isAtLimit ? styles.charCountError : isNearLimit ? styles.charCountWarning : ""
            }`}
          >
            {charCount}/{maxLength}
          </div>
        )}
      </div>
      <button
        className={styles.sendButton}
        onClick={handleSend}
        disabled={disabled || !value.trim() || isAtLimit}
        aria-label="Send message"
      >
        Send
      </button>
    </div>
  );
}

