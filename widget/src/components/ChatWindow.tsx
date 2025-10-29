import React, { useEffect, useRef } from 'react';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import type { ChatMessage as ChatMessageType } from '../types';

interface ChatWindowProps {
  messages: ChatMessageType[];
  onSendMessage: (message: string) => void;
  onFeedback?: (messageId: string, rating: 'positive' | 'negative') => void;
  onClose: () => void;
  isLoading?: boolean;
  placeholder?: string;
  welcomeMessage?: string;
  enableFeedback?: boolean;
  avatarUrl: string;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  onSendMessage,
  onFeedback,
  onClose,
  isLoading = false,
  placeholder,
  welcomeMessage = "Hi! I'm ChewieAI, your DeFi assistant. How can I help you today?",
  enableFeedback = false,
  avatarUrl,
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="chewie-chat-window">
      <div className="chewie-chat-window__header">
        <div className="chewie-chat-window__title">
          <div className="chewie-chat-window__avatar">
            {avatarUrl.startsWith('http') || avatarUrl.startsWith('/') ? (
              <img src={avatarUrl} alt="ChewieAI" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            ) : (
              <span>{avatarUrl}</span>
            )}
          </div>
          <span>ChewieAI</span>
        </div>
        <button
          onClick={onClose}
          className="chewie-chat-window__close-btn"
          title="Close chat"
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
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <div className="chewie-chat-window__messages">
        {messages.length === 0 && (
          <div className="chewie-chat-window__welcome">
            <div className="chewie-chat-window__welcome-avatar">
              {avatarUrl.startsWith('http') || avatarUrl.startsWith('/') ? (
                <img src={avatarUrl} alt="ChewieAI" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              ) : (
                <span>{avatarUrl}</span>
              )}
            </div>
            <div className="chewie-chat-window__welcome-text">
              {welcomeMessage}
            </div>
          </div>
        )}

        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message}
            onFeedback={onFeedback}
            enableFeedback={enableFeedback}
          />
        ))}

        {isLoading && (
          <div className="chewie-message chewie-message--assistant">
            <div className="chewie-message__content">
              <div className="chewie-message__loading">
                <div className="chewie-loading-dots">
                  <div className="chewie-loading-dot"></div>
                  <div className="chewie-loading-dot"></div>
                  <div className="chewie-loading-dot"></div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <ChatInput
        onSendMessage={onSendMessage}
        placeholder={placeholder}
        disabled={isLoading}
      />
    </div>
  );
};
