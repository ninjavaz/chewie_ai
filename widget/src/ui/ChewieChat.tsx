import React, { useState, useEffect, useCallback } from 'react';
import { createChewieClient } from '../core/client';
import { getTranslations } from '../core/i18n';
import type { ChewieOptions, Msg, ChewieClient } from '../core/types';
import { FloatingButton } from './FloatingButton';
import { Modal } from './Modal';
import { MessageList } from './MessageList';
import { InputBar } from './InputBar';
import '../styles/theme.css';

export type ChewieChatProps = Partial<ChewieOptions>;

export const ChewieChat: React.FC<ChewieChatProps> = (props) => {
  // Merge with defaults
  const options: ChewieOptions = {
    apiUrl: props.apiUrl || 'http://localhost:8000',
    dapp: props.dapp || 'kamino',
    lang: props.lang || 'en',
    theme: props.theme || 'dark',
    position: props.position || 'bottom-right',
    initialPrompts: props.initialPrompts || [
      'How much can I earn on 1000 USDC?',
      'What is Kamino?',
      'How does lending work?',
    ],
    mock: props.mock ?? false,
    onEvent: props.onEvent,
    token: props.token,
    avatarUrl: props.avatarUrl || '🤖',
  };

  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Msg[]>([]);
  const [isSending, setIsSending] = useState(false);
  const [client] = useState<ChewieClient>(() => createChewieClient(options));

  const t = getTranslations(options.lang);

  // Set theme attribute on mount
  useEffect(() => {
    document.documentElement.setAttribute('data-chewie-theme', options.theme || 'dark');
  }, [options.theme]);

  // Add welcome message
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        {
          id: 'welcome',
          role: 'system',
          text: t.systemMessages.welcome,
          timestamp: Date.now(),
          followups: options.initialPrompts,
        },
      ]);
    }
  }, [messages.length, t.systemMessages.welcome, options.initialPrompts]);

  const handleOpen = useCallback(() => {
    setIsOpen(true);
    options.onEvent?.({ type: 'open' });
  }, [options]);

  const handleClose = useCallback(() => {
    setIsOpen(false);
    options.onEvent?.({ type: 'close' });
  }, [options]);

  const handleSend = useCallback(
    async (text: string) => {
      const userMsg: Msg = {
        id: `user-${Date.now()}`,
        role: 'user',
        text,
        timestamp: Date.now(),
      };

      setMessages((prev) => [...prev, userMsg]);
      setIsSending(true);
      options.onEvent?.({ type: 'send', payload: { text } });

      try {
        const response = await client.ask(text);

        const assistantMsg: Msg = {
          id: `assistant-${Date.now()}`,
          role: 'assistant',
          text: response.answer,
          timestamp: Date.now(),
          sources: response.sources,
          followups: response.followups,
          earnings: response.earnings
            ? {
                yearly: response.earnings.yearly,
                monthly: response.earnings.monthly,
                apr: response.earnings.apr_value,
                updatedAt: response.earnings.updated_at,
              }
            : undefined,
        };

        setMessages((prev) => [...prev, assistantMsg]);
        options.onEvent?.({ type: 'response', payload: response });
      } catch (error) {
        const errorMsg: Msg = {
          id: `error-${Date.now()}`,
          role: 'assistant',
          text:
            error instanceof Error
              ? error.message.includes('cancelled')
                ? 'Request was cancelled.'
                : error.message.includes('timeout')
                ? t.systemMessages.networkError
                : t.systemMessages.error
              : t.systemMessages.error,
          timestamp: Date.now(),
        };

        setMessages((prev) => [...prev, errorMsg]);
        options.onEvent?.({
          type: 'error',
          payload: { error: error instanceof Error ? error.message : 'Unknown error' },
        });
      } finally {
        setIsSending(false);
      }
    },
    [client, options, t.systemMessages]
  );

  const handleFollowupClick = useCallback(
    (text: string) => {
      handleSend(text);
    },
    [handleSend]
  );

  return (
    <>
      <FloatingButton
        isOpen={isOpen}
        onClick={isOpen ? handleClose : handleOpen}
        position={options.position || 'bottom-right'}
        ariaLabel={isOpen ? t.close : 'Open Chewie Chat'}
        avatarUrl={options.avatarUrl}
      />

      {isOpen && (
        <Modal
          isOpen={isOpen}
          onClose={handleClose}
          position={options.position || 'bottom-right'}
          t={t}
          avatarUrl={options.avatarUrl}
        >
          <MessageList
            messages={messages}
            isTyping={isSending}
            t={t}
            onFollowupClick={handleFollowupClick}
            avatarUrl={options.avatarUrl}
          />
          <InputBar onSend={handleSend} disabled={isSending} t={t} />
        </Modal>
      )}
    </>
  );
};
