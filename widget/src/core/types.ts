/**
 * Core types for @chewieai/chat-widget
 */

// ============================================
// PUBLIC API TYPES
// ============================================

export type ChewieOptions = {
  /** API base URL (e.g., https://api.chewieai.com or http://localhost:8000) */
  apiUrl: string;
  /** DApp identifier */
  dapp?: 'kamino' | string;
  /** Language preference */
  lang?: 'en' | 'pl';
  /** UI theme */
  theme?: 'dark' | 'light';
  /** Widget position on screen */
  position?: 'bottom-right' | 'bottom-left';
  /** Initial suggested prompts */
  initialPrompts?: string[];
  /** Event callback for analytics */
  onEvent?: (event: ChewieEvent) => void;
  /** Optional auth token for future use */
  token?: string;
  /** Mock mode for local dev (returns canned responses) */
  mock?: boolean;
};

export type ChewieEvent =
  | { type: 'open' | 'close' | 'send' | 'response' | 'error'; payload?: any }
  | { type: 'copy' | 'cta_click'; payload: { id: string } };

// ============================================
// MESSAGE TYPES
// ============================================

export type MessageRole = 'user' | 'assistant' | 'system';

export type EarningsData = {
  yearly: number;
  monthly: number;
  apr: number;
  updatedAt?: string;
};

export type Source = string | { title: string; url: string };

export type Msg = {
  id: string;
  role: MessageRole;
  text: string;
  sources?: Source[];
  followups?: string[];
  earnings?: EarningsData;
  timestamp?: number;
};

// ============================================
// STATE TYPES
// ============================================

export type ChatState = {
  open: boolean;
  messages: Msg[];
  sending: boolean;
  error?: string;
  options: ChewieOptions;
  sessionId?: string;
};

// ============================================
// API REQUEST/RESPONSE TYPES
// ============================================

export type AskRequest = {
  query: string;
  pool_id?: string;
  amount?: number;
  currency?: string;
  context: {
    dapp: string;
    lang: string;
  };
  session_id?: string;
};

export type AskRes = {
  answer: string;
  assumptions?: Record<string, any>;
  earnings?: {
    yearly: number;
    monthly: number;
    apr_value: number;
    updated_at?: string;
  };
  confidence?: number;
  sources?: Array<{
    title: string;
    url: string;
  }>;
  followups?: string[];
  session_id?: string;
};

export type ErrorRes = {
  error: string;
  detail?: string;
};

// ============================================
// CLIENT TYPES
// ============================================

export type FetchOptions = {
  signal?: AbortSignal;
  timeout?: number;
};

export type ChewieClient = {
  ask: (query: string, options?: FetchOptions) => Promise<AskRes>;
  setSessionId: (sessionId: string) => void;
  getSessionId: () => string | undefined;
};
