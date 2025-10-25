# 🤖 @chewieai/chat-widget

Production-ready AI chat widget for DeFi dApps. Built with TypeScript, React, and optimized for developer ergonomics.

## ✨ Features

- 🎨 **Dual builds** - ESM + CJS with full TypeScript types
- 📱 **Mobile-first** - Responsive design with a11y support
- 🎯 **Three integration modes** - React component, headless client, vanilla JS
- 🌍 **i18n ready** - English & Polish built-in
- 💰 **DeFi-optimized** - Earnings cards, APR display, source citations
- 🎭 **Mock mode** - Local development without backend
- ⚡ **Lightweight** - ~35KB min+gz (React is peer dependency)
- 🔒 **Type-safe** - Full TypeScript support with exported types

## 📦 Installation

```bash
npm install @chewieai/chat-widget
# or
pnpm add @chewieai/chat-widget
# or
yarn add @chewieai/chat-widget
```

## 🚀 Quick Start

### React Integration

```tsx
import { ChewieChat } from '@chewieai/chat-widget';

function App() {
  return (
    <div>
      {/* Your dApp content */}
      
      <ChewieChat
        apiUrl={process.env.REACT_APP_CHEWIE_API}
        dapp="kamino"
        theme="dark"
        position="bottom-right"
        mock={false}
      />
    </div>
  );
}
```

### Vanilla JS (CDN)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>My DeFi App</title>
</head>
<body>
  <!-- Your content -->
  
  <!-- Auto-init with data attributes -->
  <div 
    data-chewie-api-url="https://api.chewieai.com"
    data-chewie-dapp="kamino"
    data-chewie-theme="dark"
  ></div>
  
  <script src="https://unpkg.com/@chewieai/chat-widget/dist/vanilla.js"></script>
</body>
</html>
```

Or programmatically:

```html
<script src="https://unpkg.com/@chewieai/chat-widget/dist/vanilla.js"></script>
<script>
  window.ChewieChat.init({
    apiUrl: 'https://api.chewieai.com',
    dapp: 'kamino',
    theme: 'dark',
    onEvent: (e) => console.log('Chewie:', e)
  });
</script>
```

### Headless Client (Custom UI)

```typescript
import { createChewieClient } from '@chewieai/chat-widget';

const client = createChewieClient({
  apiUrl: 'https://api.chewieai.com',
  dapp: 'kamino',
  lang: 'en',
});

// Send a query
const response = await client.ask('How much can I earn on 1000 USDC?');
console.log(response.answer);
console.log(response.earnings); // { yearly: 124, monthly: 10.33, apr: 0.124 }
```

## ⚙️ Configuration

### ChewieOptions (all integration modes)

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `apiUrl` | `string` | **required** | Backend API base URL (e.g., `http://localhost:8000`) |
| `dapp` | `string` | `'kamino'` | DApp identifier |
| `lang` | `'en' \| 'pl'` | `'en'` | Language for UI and responses |
| `theme` | `'dark' \| 'light'` | `'dark'` | Widget theme |
| `position` | `'bottom-right' \| 'bottom-left'` | `'bottom-right'` | Widget position |
| `initialPrompts` | `string[]` | Default prompts | Suggested questions to display |
| `onEvent` | `(event: ChewieEvent) => void` | `undefined` | Event callback for analytics |
| `token` | `string` | `undefined` | Optional auth token |
| `mock` | `boolean` | `false` | Enable mock mode (returns canned responses) |

## 🔌 Backend API Contract

Your FastAPI (or any) backend must implement `POST /ask`:

### Request Body

```typescript
type AskRequest = {
  query: string;              // User's question
  pool_id?: string;           // Optional: e.g., "allez-usdc"
  amount?: number;            // Optional: for earnings estimates
  currency?: string;          // Optional: default "USDC"
  context: {
    dapp: string;             // e.g., "kamino"
    lang: string;             // e.g., "en"
  };
  session_id?: string;        // UUID for session persistence
};
```

### Response (200 OK)

```typescript
type AskRes = {
  answer: string;                          // Main response text
  assumptions?: Record<string, any>;       // Assumptions made
  earnings?: {                              // For yield queries
    yearly: number;
    monthly: number;
    apr_value: number;                     // 0.124 = 12.4%
    updated_at?: string;                   // "2 hours ago"
  };
  confidence?: number;                     // 0-1
  sources?: Array<{
    title: string;
    url: string;
  }>;
  followups?: string[];                    // Suggested follow-up questions
  session_id?: string;                     // Backend can update session
};
```

### Example Responses

**Earnings query:**

```json
{
  "answer": "Based on current rates, 1,000 USDC in Allez pool earns ~$124/year.",
  "earnings": {
    "yearly": 124,
    "monthly": 10.33,
    "apr_value": 0.124,
    "updated_at": "2 hours ago"
  },
  "sources": [
    { "title": "Kamino Allez USDC", "url": "https://kamino.finance/lend/allez-usdc" }
  ],
  "followups": ["What are the risks?", "Can I withdraw anytime?"]
}
```

**General query:**

```json
{
  "answer": "Kamino Finance is a DeFi protocol on Solana...",
  "confidence": 0.95,
  "sources": [
    { "title": "Kamino Docs", "url": "https://docs.kamino.finance" }
  ]
}
```

**Uncertain:**

```json
{
  "answer": "I'm not sure about that. Here are some helpful resources:",
  "confidence": 0.3,
  "sources": [
    { "title": "Discord Support", "url": "https://discord.gg/kamino" },
    { "title": "Docs", "url": "https://docs.kamino.finance" }
  ]
}
```

## 🎨 Theming & Customization

Widget ships with Chewie AI branded dark theme. Override CSS variables to customize:

```css
:root {
  --chewie-color-primary: #225395;
  --chewie-color-secondary: #F5C751;
  --chewie-color-accent: #2DBE78;
  --chewie-radius-lg: 20px;
}
```

## 📱 Accessibility

- ✅ WCAG 2.1 AA compliant
- ✅ Keyboard navigation (Tab, Enter, Escape)
- ✅ Focus trap in modal
- ✅ Screen reader support
- ✅ Respects prefers-reduced-motion

## 🧪 Mock Mode

Test without backend by setting `mock: true`:

```tsx
<ChewieChat apiUrl="http://localhost:8000" mock={true} />
```

## 🔄 Events

```typescript
onEvent={(event) => {
  if (event.type === 'send') analytics.track('query', event.payload);
}}
```

## 🛠️ Development

```bash
pnpm install
pnpm build      # Dual ESM+CJS output
pnpm test       # Vitest + a11y tests
pnpm dev        # Watch mode
```

## 📦 Bundle Size

~35KB min+gz (React peer dep excluded)

## 📄 License

MIT

## 📞 Support

- 🐛 [GitHub Issues](https://github.com/chewieai/chat-widget/issues)
- 💬 [Discord](https://discord.gg/kamino)
