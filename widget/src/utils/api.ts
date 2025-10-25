import type { ApiRequest, ApiRes, FeedbackRequest } from '../types';

export class ChewieApiClient {
  private endpoint: string;

  constructor(endpoint: string = 'https://chewie.ai/api/ask') {
    this.endpoint = endpoint;
  }

  async ask(request: ApiRequest): Promise<ApiRes> {
    try {
      const response = await fetch(this.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('ChewieAI API Error:', error);
      return {
        answer: 'Sorry, I encountered an error while processing your request. Please try again.',
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }

  async sendFeedback(feedback: FeedbackRequest): Promise<void> {
    try {
      const feedbackEndpoint = this.endpoint.replace('/ask', '/feedback');
      await fetch(feedbackEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(feedback),
      });
    } catch (error) {
      console.error('Feedback Error:', error);
    }
  }
}
