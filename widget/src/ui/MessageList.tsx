import React, { useEffect, useRef } from 'react';
import type { Msg } from '../core/types';
import type { Translations } from '../core/i18n';
import { EarningsCard } from './EarningsCard';
import styles from './MessageList.module.css';

export type MessageListProps = {
  messages: Msg[];
  isTyping: boolean;
  t: Translations;
  onFollowupClick?: (text: string) => void;
};

export const MessageList: React.FC<MessageListProps> = ({
  messages,
  isTyping,
  t,
  onFollowupClick,
}) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  return (
    <div className={styles.container}>
      <div className={styles.messages}>
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`${styles.message} ${styles[msg.role]}`}
          >
            <div className={styles.bubble}>
              <div className={styles.text}>{msg.text}</div>
              
              {msg.earnings && (
                <EarningsCard earnings={msg.earnings} t={t} />
              )}

              {msg.sources && msg.sources.length > 0 && (
                <div className={styles.sources}>
                  <div className={styles.sourcesTitle}>{t.sources}:</div>
                  <ul className={styles.sourcesList}>
                    {msg.sources.map((source, idx) => {
                      // Handle both string and object sources
                      const isObject = typeof source === 'object' && source !== null;
                      const title = isObject ? (source as any).title : `Source ${idx + 1}`;
                      const url = isObject ? (source as any).url : source;

                      return (
                        <li key={idx}>
                          <a
                            href={url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className={styles.sourceLink}
                          >
                            {title}
                          </a>
                        </li>
                      );
                    })}
                  </ul>
                </div>
              )}

              {msg.followups && msg.followups.length > 0 && (
                <div className={styles.followups}>
                  {msg.followups.map((followup, idx) => (
                    <button
                      key={idx}
                      type="button"
                      className={styles.followupChip}
                      onClick={() => onFollowupClick?.(followup)}
                    >
                      {followup}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {msg.timestamp && (
              <div className={styles.timestamp}>
                {new Date(msg.timestamp).toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </div>
            )}
          </div>
        ))}

        {isTyping && (
          <div className={`${styles.message} ${styles.assistant}`}>
            <div className={styles.bubble}>
              <div className={styles.typing}>
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>
    </div>
  );
};
