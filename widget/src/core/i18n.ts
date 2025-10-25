/**
 * Internationalization dictionary
 */

export type Lang = 'en' | 'pl';

export type Translations = {
  placeholder: string;
  send: string;
  close: string;
  minimize: string;
  copy: string;
  copied: string;
  typing: string;
  error: string;
  retry: string;
  sources: string;
  suggestedPrompts: string;
  earnings: {
    title: string;
    yearly: string;
    monthly: string;
    apr: string;
    updated: string;
  };
  systemMessages: {
    welcome: string;
    error: string;
    networkError: string;
  };
};

const en: Translations = {
  placeholder: 'Ask Chewie anything…',
  send: 'Send',
  close: 'Close chat',
  minimize: 'Minimize',
  copy: 'Copy',
  copied: 'Copied!',
  typing: 'Chewie is typing...',
  error: 'Error',
  retry: 'Retry',
  sources: 'Sources',
  suggestedPrompts: 'Try asking:',
  earnings: {
    title: 'Earnings Estimate',
    yearly: 'per year',
    monthly: 'per month',
    apr: 'APR',
    updated: 'Updated',
  },
  systemMessages: {
    welcome: "Hi! I'm Chewie, your DeFi assistant. Ask me anything about Kamino!",
    error: 'Sorry, something went wrong. Please try again.',
    networkError: 'Network error. Please check your connection.',
  },
};

const pl: Translations = {
  placeholder: 'Zapytaj Chewie o cokolwiek…',
  send: 'Wyślij',
  close: 'Zamknij chat',
  minimize: 'Minimalizuj',
  copy: 'Kopiuj',
  copied: 'Skopiowano!',
  typing: 'Chewie pisze...',
  error: 'Błąd',
  retry: 'Ponów',
  sources: 'Źródła',
  suggestedPrompts: 'Spróbuj zapytać:',
  earnings: {
    title: 'Szacunkowe zarobki',
    yearly: 'rocznie',
    monthly: 'miesięcznie',
    apr: 'APR',
    updated: 'Zaktualizowano',
  },
  systemMessages: {
    welcome: 'Cześć! Jestem Chewie, Twój asystent DeFi. Zapytaj mnie o Kamino!',
    error: 'Przepraszam, coś poszło nie tak. Spróbuj ponownie.',
    networkError: 'Błąd sieci. Sprawdź swoje połączenie.',
  },
};

const translations: Record<Lang, Translations> = {
  en,
  pl,
};

export function getTranslations(lang: Lang = 'en'): Translations {
  return translations[lang] || translations.en;
}
