import React from 'react';
import styles from './FloatingButton.module.css';

export type FloatingButtonProps = {
  isOpen: boolean;
  onClick: () => void;
  position: 'bottom-right' | 'bottom-left';
  ariaLabel: string;
};

export const FloatingButton: React.FC<FloatingButtonProps> = ({
  isOpen,
  onClick,
  position,
  ariaLabel,
}) => {
  return (
    <button
      className={`${styles.button} ${styles[position]} ${isOpen ? styles.open : ''}`}
      onClick={onClick}
      aria-label={ariaLabel}
      aria-expanded={isOpen}
      type="button"
    >
      {isOpen ? (
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <line x1="18" y1="6" x2="6" y2="18" />
          <line x1="6" y1="6" x2="18" y2="18" />
        </svg>
      ) : (
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
        </svg>
      )}
    </button>
  );
};
