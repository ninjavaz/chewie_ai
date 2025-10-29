import React, { useState, useEffect } from 'react';
import styles from './FloatingButton.module.css';

export type FloatingButtonProps = {
  isOpen: boolean;
  onClick: () => void;
  position: 'bottom-right' | 'bottom-left';
  ariaLabel: string;
  avatarUrl: string;
};

export const FloatingButton: React.FC<FloatingButtonProps> = ({
  isOpen,
  onClick,
  position,
  ariaLabel,
  avatarUrl,
}) => {
  const [showTooltip, setShowTooltip] = useState(false);
  const [hasClicked, setHasClicked] = useState(false);

  useEffect(() => {
    // Show tooltip after 2 seconds if user hasn't clicked yet
    if (!hasClicked) {
      const timer = setTimeout(() => {
        setShowTooltip(true);
      }, 2000);

      return () => {
        clearTimeout(timer);
      };
    }
  }, [hasClicked]);

  const handleClick = () => {
    setHasClicked(true);
    setShowTooltip(false);
    onClick();
  };

  return (
    <>
      {showTooltip && !hasClicked && (
        <div className={`${styles.tooltip} ${position === 'bottom-right' ? styles.right : styles.left}`}>
          💡 Confused? Let me explain!
        </div>
      )}
      <button
        className={`${styles.button} ${styles[position]} ${isOpen ? styles.open : ''}`}
        onClick={handleClick}
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
        avatarUrl?.startsWith('http') || avatarUrl?.startsWith('/') ? (
          <img src={avatarUrl} alt="ChewieAI" className={styles.avatarImage} />
        ) : (
          <span className={styles.avatarEmoji}>{avatarUrl || '🤖'}</span>
        )
      )}
      </button>
    </>
  );
};
