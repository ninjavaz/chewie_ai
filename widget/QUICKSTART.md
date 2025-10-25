# 🚀 Quickstart Guide

Get the Chewie chat widget running in 5 minutes.

## Step 1: Install Dependencies

```bash
cd widget
pnpm install
```

## Step 2: Build the Library

```bash
pnpm build
```

This creates:
- `dist/index.js` (ESM)
- `dist/index.cjs` (CommonJS)
- `dist/index.d.ts` (TypeScript types)
- `dist/vanilla.js` (Vanilla JS embed)
- `dist/styles.css` (CSS)

## Step 3: Run Examples

### React Example

```bash
cd examples/react
pnpm install
pnpm dev
```

Open http://localhost:3000

### Vanilla JS Example

```bash
cd examples/vanilla
# Use any static server, e.g.:
python -m http.server 3001
# or
npx serve .
```

Open http://localhost:3001

## Step 4: Test Mock Mode

The examples run in **mock mode** by default (no backend needed). Click the chat button and try:

- "How much can I earn on 1000 USDC?"
- "What is Kamino?"
- "When does staking end?"

## Step 5: Connect to Your Backend

### Update .env

```bash
# examples/react/.env.local
VITE_CHEWIE_API_URL=https://your-backend.com
```

### Update Component

```tsx
<ChewieChat
  apiUrl={import.meta.env.VITE_CHEWIE_API_URL}
  dapp="kamino"
  mock={false}  // Disable mock mode
/>
```

Your backend needs to implement `POST /ask` (see README.md for full API spec).

## Running Tests

```bash
# Unit tests
pnpm test

# With coverage
pnpm test --coverage

# Watch mode
pnpm test:watch
```

## Next Steps

1. **Customize theme** - Edit CSS variables in `src/styles/theme.css`
2. **Add languages** - Extend `src/core/i18n.ts`
3. **Integrate analytics** - Use `onEvent` callback
4. **Deploy** - Build and publish to npm

## Troubleshooting

**"Module not found" in React example:**
- Ensure you ran `pnpm build` in the root widget directory
- Check that `pnpm install` was run in examples/react

**TypeScript errors:**
- Run `pnpm type-check` to see detailed errors
- Ensure you have TypeScript 5.2+ installed

**Tests failing:**
- Install vitest globally: `pnpm add -g vitest`
- Clear node_modules and reinstall: `rm -rf node_modules && pnpm install`

## Development Workflow

```bash
# Watch mode for rapid development
pnpm dev

# In another terminal, run example
cd examples/react && pnpm dev

# Make changes to src/ - auto-rebuilds
# Refresh browser to see changes
```

Happy building! 🎉
