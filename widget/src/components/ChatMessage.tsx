import React from 'react';
import type { ChatMessage as ChatMessageType } from '../types';

interface ChatMessageProps {
  message: ChatMessageType;
  onFeedback?: (messageId: string, rating: 'positive' | 'negative') => void;
  enableFeedback?: boolean;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({
  message,
  onFeedback,
  enableFeedback = false,
}) => {
  const isUser = message.type === 'user';
  const timestamp = new Date(message.timestamp).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <div className={`chewie-message ${isUser ? 'chewie-message--user' : 'chewie-message--assistant'}`}>
      <div className="chewie-message__content">
        <div className="chewie-message__text">{message.content}</div>
        
        {message.sources && message.sources.length > 0 && (
          <div className="chewie-message__sources">
            <div className="chewie-message__sources-title">Sources:</div>
            {message.sources.map((source, index) => (
              <a
                key={index}
                href={source}
                target="_blank"
                rel="noopener noreferrer"
                className="chewie-message__source-link"
              >
                {source}
              </a>
            ))}
          </div>
        )}
      </div>
      
      <div className="chewie-message__meta">
        <span className="chewie-message__timestamp">{timestamp}</span>
        
        {!isUser && enableFeedback && onFeedback && (
          <div className="chewie-message__feedback">
            <button
              className="chewie-message__feedback-btn chewie-message__feedback-btn--positive"
              onClick={() => onFeedback(message.id, 'positive')}
              title="Helpful"
            >
              👍
            </button>
            <button
              className="chewie-message__feedback-btn chewie-message__feedback-btn--negative"
              onClick={() => onFeedback(message.id, 'negative')}
              title="Not helpful"
            >
              👎
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
