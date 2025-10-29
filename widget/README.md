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
| `avatarUrl` | `string` | `'🤖'` | Custom avatar URL or emoji for assistant messages |

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

The widget is fully customizable using CSS custom properties. Override variables in your CSS to match your brand:

### Quick Example

```css
:root {
  /* Brand colors */
  --chewie-button-primary-bg: #FF6B6B;
  --chewie-button-primary-bg-hover: #EE5A52;
  --chewie-message-user-bg: #4A90E2;
  --chewie-followup-bg: #FFD93D;
}
```

### Color Variables

#### Chat UI Colors
```css
/* Header */
--chewie-chat-header-bg: #052346;

/* Messages area */
--chewie-chat-messages-bg: #E8EDF2;
--chewie-message-user-bg: #3B5998;
--chewie-message-user-text: #FFFFFF;
--chewie-message-assistant-bg: #FFFFFF;
--chewie-message-assistant-text: #2C3E50;
--chewie-message-avatar-bg: #FFFFFF;

/* Follow-up chips */
--chewie-followup-bg: #F5C751;
--chewie-followup-bg-hover: #F8D555;
--chewie-followup-text: #2C3E50;

/* Input area */
--chewie-chat-input-bg: #FFFFFF;
--chewie-chat-input-field-bg: #F5F7FA;
--chewie-chat-input-border: #E0E5EB;
--chewie-placeholder-text: #9CA3AF;

/* Buttons */
--chewie-button-primary-bg: #3B5998;
--chewie-button-primary-bg-hover: #2F4779;
--chewie-button-primary-text: #FFFFFF;
```

### Dimension Variables

```css
/* Avatar & Icons */
--chewie-avatar-size: 40px;
--chewie-avatar-radius: 8px;
--chewie-icon-size: 20px;

/* Messages */
--chewie-message-padding: 14px 16px;
--chewie-message-radius: 16px;
--chewie-message-radius-corner: 4px;
--chewie-message-font-size: 15px;
--chewie-message-gap: 8px;

/* Input */
--chewie-input-padding: 10px 16px;
--chewie-input-radius: 24px;
--chewie-input-font-size: 15px;

/* Buttons & Chips */
--chewie-action-button-size: 36px;
--chewie-followup-padding: 10px 16px;
--chewie-followup-radius: 20px;
--chewie-followup-font-size: 14px;

/* Modal */
--chewie-modal-width: 400px;
--chewie-modal-height: 600px;
--chewie-modal-bottom: 100px;
--chewie-modal-spacing: 24px;

/* Typography */
--chewie-font-heading: 'Poppins', sans-serif;
--chewie-font-body: 'Inter', sans-serif;

/* Animations */
--chewie-animation-duration: 0.3s;
```

### Example Themes

#### Dark Theme
```css
:root {
  --chewie-chat-header-bg: #1a1a1a;
  --chewie-chat-messages-bg: #2d2d2d;
  --chewie-chat-input-bg: #1a1a1a;
  --chewie-chat-input-field-bg: #3d3d3d;
  --chewie-message-assistant-bg: #3d3d3d;
  --chewie-message-assistant-text: #ffffff;
  --chewie-button-primary-bg: #0084ff;
}
```

#### Compact Mode
```css
:root {
  --chewie-modal-width: 350px;
  --chewie-modal-height: 500px;
  --chewie-avatar-size: 32px;
  --chewie-message-font-size: 14px;
  --chewie-action-button-size: 32px;
}
```

### Using Your Brand Colors

```css
:root {
  --chewie-button-primary-bg: var(--your-brand-primary);
  --chewie-button-primary-bg-hover: var(--your-brand-primary-dark);
  --chewie-message-user-bg: var(--your-brand-accent);
  --chewie-followup-bg: var(--your-brand-secondary);
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
