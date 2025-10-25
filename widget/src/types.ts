export interface ChewieWidgetProps {
  /** API endpoint for the ChewieAI backend */
  endpoint?: string;
  /** Protocol identifier (e.g., "aave", "compound", "uniswap") */
  protocol?: string;
  /** Widget theme */
  theme?: 'light' | 'dark' | 'auto';
  /** Widget position on screen */
  position?: 'bottom-right' | 'bottom-left' | 'top-right' | 'top-left';
  /** Custom user identifier */
  userId?: string;
  /** Language for responses */
  language?: 'en' | 'pl' | 'es' | 'zh' | 'fr' | 'de';
  /** Custom CSS class name */
  className?: string;
  /** Custom styles */
  style?: React.CSSProperties;
  /** Whether to show the widget initially */
  defaultOpen?: boolean;
  /** Custom placeholder text */
  placeholder?: string;
  /** Custom welcome message */
  welcomeMessage?: string;
  /** Enable feedback buttons */
  enableFeedback?: boolean;
  /** Custom icon URL */
  iconUrl?: string;
  /** Maximum chat history length */
  maxHistory?: number;
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: number;
  sources?: string[];
}

export interface ApiRequest {
  question: string;
  user: string;
  lang: string;
  protocol?: string;
}

export interface ApiRes {
  answer: string;
  sources?: string[];
  error?: string;
}

export interface FeedbackRequest {
  messageId: string;
  rating: 'positive' | 'negative';
  comment?: string;
}
