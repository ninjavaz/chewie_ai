import type { ChatMessage } from '../types';

const STORAGE_KEY = 'chewie-chat-history';
const MAX_HISTORY_DEFAULT = 50;

export class ChatStorage {
  private maxHistory: number;

  constructor(maxHistory: number = MAX_HISTORY_DEFAULT) {
    this.maxHistory = maxHistory;
  }

  saveMessages(messages: ChatMessage[]): void {
    try {
      const trimmedMessages = messages.slice(-this.maxHistory);
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(trimmedMessages));
    } catch (error) {
      console.warn('Failed to save chat history:', error);
    }
  }

  loadMessages(): ChatMessage[] {
    try {
      const stored = sessionStorage.getItem(STORAGE_KEY);
      if (!stored) return [];
      
      const messages = JSON.parse(stored);
      return Array.isArray(messages) ? messages : [];
    } catch (error) {
      console.warn('Failed to load chat history:', error);
      return [];
    }
  }

  clearMessages(): void {
    try {
      sessionStorage.removeItem(STORAGE_KEY);
    } catch (error) {
      console.warn('Failed to clear chat history:', error);
    }
  }

  generateUserId(): string {
    const stored = sessionStorage.getItem('chewie-user-id');
    if (stored) return stored;

    const userId = `anon-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    sessionStorage.setItem('chewie-user-id', userId);
    return userId;
  }
}
