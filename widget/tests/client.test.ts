import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { createChewieClient } from '../src/core/client';
import type { ChewieOptions, AskRes } from '../src/core/types';

describe('ChewieClient', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn();
    global.fetch = fetchMock;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Mock Mode', () => {
    it('should return mock response for general query', async () => {
      const client = createChewieClient({
        apiUrl: 'http://localhost:8000',
        mock: true,
      });

      const response = await client.ask('What is Kamino?');

      expect(response.answer).toContain('Kamino Finance');
      expect(response.sources).toBeDefined();
      expect(response.followups).toBeDefined();
    });

    it('should return earnings mock for yield query', async () => {
      const client = createChewieClient({
        apiUrl: 'http://localhost:8000',
        mock: true,
      });

      const response = await client.ask('How much can I earn on 1000 USDC?');

      expect(response.earnings).toBeDefined();
      expect(response.earnings?.yearly).toBe(124);
      expect(response.earnings?.apr_value).toBe(0.124);
    });

    it('should return uncertain response for specific queries', async () => {
      const client = createChewieClient({
        apiUrl: 'http://localhost:8000',
        mock: true,
      });

      const response = await client.ask('When exactly does this happen?');

      expect(response.confidence).toBeLessThan(0.5);
      expect(response.sources?.length).toBeGreaterThan(0);
    });
  });

  describe('Real API Mode', () => {
    it('should make POST request to /ask endpoint', async () => {
      const mockResponse: AskRes = {
        answer: 'Test answer',
        confidence: 0.9,
        sources: [{ title: 'Test', url: 'https://test.com' }],
      };

      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const client = createChewieClient({
        apiUrl: 'http://localhost:8000',
        dapp: 'kamino',
        lang: 'en',
      });

      const response = await client.ask('Test query');

      expect(fetchMock).toHaveBeenCalledWith(
        'http://localhost:8000/ask',
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
          }),
          body: expect.stringContaining('Test query'),
        })
      );

      expect(response.answer).toBe('Test answer');
    });

    it('should include auth token if provided', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ answer: 'Test' }),
      });

      const client = createChewieClient({
        apiUrl: 'http://localhost:8000',
        token: 'test-token-123',
      });

      await client.ask('Test query');

      const callArgs = fetchMock.mock.calls[0];
      const headers = callArgs[1].headers;

      expect(headers.Authorization).toBe('Bearer test-token-123');
    });

    it('should handle HTTP errors gracefully', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => ({ error: 'Internal Server Error' }),
      });

      const client = createChewieClient({
        apiUrl: 'http://localhost:8000',
      });

      await expect(client.ask('Test query')).rejects.toThrow('Internal Server Error');
    });

    it('should handle network errors', async () => {
      fetchMock.mockRejectedValueOnce(new Error('Network failed'));

      const client = createChewieClient({
        apiUrl: 'http://localhost:8000',
      });

      await expect(client.ask('Test query')).rejects.toThrow('Network failed');
    });

    it('should handle request timeout', async () => {
      fetchMock.mockImplementationOnce(
        () =>
          new Promise((_, reject) => {
            setTimeout(() => {
              const error = new Error('The operation was aborted');
              error.name = 'AbortError';
              reject(error);
            }, 100);
          })
      );

      const client = createChewieClient({
        apiUrl: 'http://localhost:8000',
      });

      await expect(client.ask('Test query', { timeout: 50 })).rejects.toThrow('Request was cancelled');
    });

    it('should respect abort signal', async () => {
      fetchMock.mockImplementationOnce(
        () =>
          new Promise((_, reject) => {
            setTimeout(() => {
              const error = new Error('The operation was aborted');
              error.name = 'AbortError';
              reject(error);
            }, 100);
          })
      );

      const client = createChewieClient({
        apiUrl: 'http://localhost:8000',
      });

      const controller = new AbortController();
      const promise = client.ask('Test query', { signal: controller.signal });

      setTimeout(() => controller.abort(), 50);

      await expect(promise).rejects.toThrow('Request was cancelled');
    });
  });

  describe('Session Management', () => {
    it('should generate and persist session ID', async () => {
      fetchMock.mockResolvedValue({
        ok: true,
        json: async () => ({ answer: 'Test' }),
      });

      const client = createChewieClient({
        apiUrl: 'http://localhost:8000',
      });

      await client.ask('First query');
      const sessionId1 = client.getSessionId();
      
      await client.ask('Second query');
      const sessionId2 = client.getSessionId();

      expect(sessionId1).toBeDefined();
      expect(sessionId1).toBe(sessionId2);
    });

    it('should allow setting custom session ID', async () => {
      const client = createChewieClient({
        apiUrl: 'http://localhost:8000',
      });

      client.setSessionId('custom-session-123');

      expect(client.getSessionId()).toBe('custom-session-123');
    });

    it('should update session ID from backend response', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          answer: 'Test',
          session_id: 'backend-session-456',
        }),
      });

      const client = createChewieClient({
        apiUrl: 'http://localhost:8000',
      });

      await client.ask('Test query');

      expect(client.getSessionId()).toBe('backend-session-456');
    });
  });
});
