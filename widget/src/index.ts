/**
 * @chewieai/chat-widget
 * Production-ready chat widget for DeFi dApps
 */

// React component
export { ChewieChat } from './ui/ChewieChat';
export type { ChewieChatProps } from './ui/ChewieChat';

// Headless client for custom implementations
export { createChewieClient } from './core/client';

// Types
export type {
  ChewieOptions,
  ChewieEvent,
  ChewieClient,
  Msg,
  MessageRole,
  EarningsData,
  Source,
  AskRequest,
  AskRes,
  ErrorRes,
} from './core/types';

// Utilities
export { getTranslations } from './core/i18n';
export type { Lang, Translations } from './core/i18n';
