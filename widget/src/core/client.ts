/**
 * Headless Chewie client - handles API communication
 */

import type { ChewieOptions, AskRequest, AskRes, ErrorRes, FetchOptions, ChewieClient } from './types';

const DEFAULT_TIMEOUT = 30000; // 30 seconds

/**
 * Mock responses for local development
 */
const MOCK_RESPONSES: AskRes[] = [
  {
    answer: 'Kamino Finance is a DeFi protocol on Solana offering automated liquidity management and lending services. It helps users optimize their yields through concentrated liquidity strategies.',
    confidence: 0.95,
    sources: [
      { title: 'Kamino Docs - Overview', url: 'https://docs.kamino.finance' },
      { title: 'Kamino FAQ', url: 'https://kamino.finance/faq' },
    ],
    followups: [
      'How do I deposit into Kamino?',
      'What are the fees?',
      'Is Kamino audited?',
    ],
  },
  {
    answer: 'Based on current rates, depositing 1,000 USDC into the Allez USDC pool can earn you approximately $124 per year.',
    earnings: {
      yearly: 124,
      monthly: 10.33,
      apr_value: 0.124,
      updated_at: '2 hours ago',
    },
    confidence: 0.88,
    assumptions: {
      pool: 'allez-usdc',
      amount: 1000,
      currency: 'USDC',
    },
    sources: [
      { title: 'Kamino Allez USDC Pool', url: 'https://kamino.finance/lend/allez-usdc' },
    ],
    followups: [
      'How often are rewards distributed?',
      'What are the risks?',
      'Can I withdraw anytime?',
    ],
  },
  {
    answer: "I'm not entirely sure about that specific detail. Here are some helpful resources:",
    confidence: 0.3,
    sources: [
      { title: 'Kamino Discord Support', url: 'https://discord.gg/kamino' },
      { title: 'Kamino Documentation', url: 'https://docs.kamino.finance' },
      { title: 'Kamino Help Center', url: 'https://help.kamino.finance' },
    ],
    followups: [
      'Tell me about Kamino pools',
      'How does lending work?',
      'What is APR?',
    ],
  },
];

function getMockResponse(query: string): AskRes {
  const lowerQuery = query.toLowerCase();
  
  // Earnings query
  if (
    (lowerQuery.includes('earn') || lowerQuery.includes('yield') || lowerQuery.includes('apr')) &&
    (lowerQuery.includes('usdc') || /\d+/.test(query))
  ) {
    return MOCK_RESPONSES[1];
  }
  
  // Uncertain response
  if (lowerQuery.includes('specific') || lowerQuery.includes('exact') || lowerQuery.includes('when')) {
    return MOCK_RESPONSES[2];
  }
  
  // Default general response
  return MOCK_RESPONSES[0];
}

/**
 * Creates a Chewie client instance
 */
export function createChewieClient(options: ChewieOptions): ChewieClient {
  let sessionId: string | undefined;

  /**
   * Generates a UUID v4
   */
  function generateUUID(): string {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = (Math.random() * 16) | 0;
      const v = c === 'x' ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  }

  /**
   * Performs the API request with timeout and abort support
   */
  async function fetchWithTimeout(
    url: string,
    init: RequestInit,
    timeout: number,
    signal?: AbortSignal
  ): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    // Combine external signal with timeout signal
    if (signal) {
      signal.addEventListener('abort', () => controller.abort());
    }

    try {
      const response = await fetch(url, {
        ...init,
        signal: controller.signal,
      });
      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      clearTimeout(timeoutId);
      throw error;
    }
  }

  /**
   * Main ask method - sends query to backend
   */
  async function ask(query: string, fetchOptions?: FetchOptions): Promise<AskRes> {
    // Mock mode
    if (options.mock) {
      // Simulate network delay
      await new Promise((resolve) => setTimeout(resolve, 800 + Math.random() * 400));
      return getMockResponse(query);
    }

    // Ensure session ID exists
    if (!sessionId) {
      sessionId = generateUUID();
    }

    const requestBody: AskRequest = {
      query,
      context: {
        dapp: options.dapp || 'kamino',
        lang: options.lang || 'en',
      },
      session_id: sessionId,
    };

    const timeout = fetchOptions?.timeout || DEFAULT_TIMEOUT;
    const url = `${options.apiUrl}/ask`;

    try {
      const response = await fetchWithTimeout(
        url,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(options.token && { Authorization: `Bearer ${options.token}` }),
          },
          body: JSON.stringify(requestBody),
        },
        timeout,
        fetchOptions?.signal
      );

      if (!response.ok) {
        const errorData: ErrorRes = await response.json().catch(() => ({
          error: `HTTP ${response.status}`,
        }));
        throw new Error(errorData.error || `Request failed with status ${response.status}`);
      }

      const data: AskRes = await response.json();
      
      // Update session ID if backend provides one
      if (data.session_id) {
        sessionId = data.session_id;
      }

      return data;
    } catch (error) {
      // Handle abort
      if (error instanceof Error && error.name === 'AbortError') {
        throw new Error('Request was cancelled');
      }

      // Handle timeout
      if (error instanceof Error && error.message.includes('abort')) {
        throw new Error('Request timed out');
      }

      // Re-throw with better message
      if (error instanceof Error) {
        throw error;
      }

      throw new Error('Network request failed');
    }
  }

  function setSessionId(id: string): void {
    sessionId = id;
  }

  function getSessionId(): string | undefined {
    return sessionId;
  }

  return {
    ask,
    setSessionId,
    getSessionId,
  };
}
