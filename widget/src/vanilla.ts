/**
 * Vanilla JavaScript embed for non-React sites
 * Usage: <script src="https://unpkg.com/@chewieai/chat-widget/dist/vanilla.js"></script>
 */

import React from 'react';
import { createRoot } from 'react-dom/client';
import { ChewieChat } from './ui/ChewieChat';
import type { ChewieOptions } from './core/types';

declare global {
  interface Window {
    ChewieChat?: {
      init: (options: Partial<ChewieOptions>) => void;
      destroy: () => void;
    };
  }
}

let root: ReturnType<typeof createRoot> | null = null;
let container: HTMLElement | null = null;

function init(options: Partial<ChewieOptions> = {}): void {
  // Clean up existing instance
  if (root) {
    destroy();
  }

  // Create container
  container = document.createElement('div');
  container.id = 'chewie-chat-widget';
  document.body.appendChild(container);

  // Mount React component
  root = createRoot(container);
  root.render(React.createElement(ChewieChat, options));
}

function destroy(): void {
  if (root && container) {
    root.unmount();
    container.remove();
    root = null;
    container = null;
  }
}

// Auto-init if element with data-chewie-api-url exists
if (typeof window !== 'undefined') {
  window.ChewieChat = {
    init,
    destroy,
  };

  // Auto-init from script tag attributes or data element
  window.addEventListener('DOMContentLoaded', () => {
    const autoInitElement = document.querySelector('[data-chewie-api-url]');
    if (autoInitElement) {
      const options: Partial<ChewieOptions> = {
        apiUrl: autoInitElement.getAttribute('data-chewie-api-url') || undefined,
        dapp: (autoInitElement.getAttribute('data-chewie-dapp') as any) || undefined,
        lang: (autoInitElement.getAttribute('data-chewie-lang') as any) || undefined,
        theme: (autoInitElement.getAttribute('data-chewie-theme') as any) || undefined,
        position: (autoInitElement.getAttribute('data-chewie-position') as any) || undefined,
        mock: autoInitElement.getAttribute('data-chewie-mock') === 'true',
      };
      init(options);
    }
  });
}

export { init, destroy };
