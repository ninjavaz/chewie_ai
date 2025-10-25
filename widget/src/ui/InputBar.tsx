import React, { useState, useRef, KeyboardEvent } from 'react';
import type { Translations } from '../core/i18n';
import styles from './InputBar.module.css';

export type InputBarProps = {
  onSend: (message: string) => void;
  disabled: boolean;
  t: Translations;
};

export const InputBar: React.FC<InputBarProps> = ({ onSend, disabled, t }) => {
  const [value, setValue] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    const trimmed = value.trim();
    if (trimmed && !disabled) {
      onSend(trimmed);
      setValue('');
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setValue(e.target.value);
    
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.inputWrapper}>
        <textarea
          ref={textareaRef}
          className={styles.textarea}
          value={value}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder={t.placeholder}
          disabled={disabled}
          rows={1}
          aria-label={t.placeholder}
        />
        <button
          type="button"
          className={styles.sendButton}
          onClick={handleSubmit}
          disabled={disabled || !value.trim()}
          aria-label={t.send}
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="22" y1="2" x2="11" y2="13" />
            <polygon points="22 2 15 22 11 13 2 9 22 2" />
          </svg>
        </button>
      </div>
      <div className={styles.hint}>
        {t.placeholder} • Shift+Enter {t.placeholder.includes('new line') ? '' : 'for new line'}
      </div>
    </div>
  );
};
