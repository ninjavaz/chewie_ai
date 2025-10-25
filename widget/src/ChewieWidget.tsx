import React, { useState, useEffect, useCallback } from 'react';
import { clsx } from 'clsx';
import { ChatWindow } from './components/ChatWindow';
import { ChewieApiClient } from './utils/api';
import { ChatStorage } from './utils/storage';
import type { ChewieWidgetProps, ChatMessage } from './types';

export const ChewieWidget: React.FC<ChewieWidgetProps> = ({
  endpoint = 'https://chewie.ai/api/ask',
  protocol,
  theme = 'auto',
  position = 'bottom-right',
  userId,
  language = 'en',
  className,
  style,
  defaultOpen = false,
  placeholder,
  welcomeMessage,
  enableFeedback = false,
  iconUrl,
  maxHistory = 50,
}) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [apiClient] = useState(() => new ChewieApiClient(endpoint));
  const [storage] = useState(() => new ChatStorage(maxHistory));
  const [currentUserId] = useState(() => userId || storage.generateUserId());

  // Load messages from storage on mount
  useEffect(() => {
    const savedMessages = storage.loadMessages();
    setMessages(savedMessages);
  }, [storage]);

  // Save messages to storage when they change
  useEffect(() => {
    if (messages.length > 0) {
      storage.saveMessages(messages);
    }
  }, [messages, storage]);

  // Auto-detect theme
  useEffect(() => {
    if (theme === 'auto') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const updateTheme = () => {
        document.documentElement.setAttribute(
          'data-chewie-theme',
          mediaQuery.matches ? 'dark' : 'light'
        );
      };
      
      updateTheme();
      mediaQuery.addEventListener('change', updateTheme);
      
      return () => mediaQuery.removeEventListener('change', updateTheme);
    } else {
      document.documentElement.setAttribute('data-chewie-theme', theme);
    }
  }, [theme]);

  const handleSendMessage = useCallback(async (content: string) => {
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      type: 'user',
      content,
      timestamp: Date.now(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await apiClient.ask({
        question: content,
        user: currentUserId,
        lang: language,
        protocol,
      });

      const assistantMessage: ChatMessage = {
        id: `assistant-${Date.now()}`,
        type: 'assistant',
        content: response.answer,
        timestamp: Date.now(),
        sources: response.sources,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Failed to send message:', error);
      
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        type: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: Date.now(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [apiClient, currentUserId, language, protocol]);

  const handleFeedback = useCallback(async (messageId: string, rating: 'positive' | 'negative') => {
    try {
      await apiClient.sendFeedback({
        messageId,
        rating,
      });
    } catch (error) {
      console.error('Failed to send feedback:', error);
    }
  }, [apiClient]);

  const handleToggle = useCallback(() => {
    setIsOpen(prev => !prev);
  }, []);

  const handleClose = useCallback(() => {
    setIsOpen(false);
  }, []);

  const positionClasses = {
    'bottom-right': 'chewie-widget--bottom-right',
    'bottom-left': 'chewie-widget--bottom-left',
    'top-right': 'chewie-widget--top-right',
    'top-left': 'chewie-widget--top-left',
  };

  return (
    <div
      className={clsx(
        'chewie-widget',
        positionClasses[position],
        className
      )}
      style={style}
    >
      {isOpen && (
        <ChatWindow
          messages={messages}
          onSendMessage={handleSendMessage}
          onFeedback={enableFeedback ? handleFeedback : undefined}
          onClose={handleClose}
          isLoading={isLoading}
          placeholder={placeholder}
          welcomeMessage={welcomeMessage}
          enableFeedback={enableFeedback}
        />
      )}

      <button
        onClick={handleToggle}
        className={clsx(
          'chewie-widget__toggle-btn',
          isOpen && 'chewie-widget__toggle-btn--open'
        )}
        title={isOpen ? 'Close chat' : 'Open chat'}
      >
        {iconUrl ? (
          <img src={iconUrl} alt="ChewieAI" className="chewie-widget__icon" />
        ) : (
          <div className="chewie-widget__default-icon">
            {isOpen ? '✕' : '🤖'}
          </div>
        )}
      </button>
    </div>
  );
};
