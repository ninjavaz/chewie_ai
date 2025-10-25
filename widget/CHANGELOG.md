# Changelog

All notable changes to @chewieai/chat-widget will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-24

### Added

- 🎉 Initial release
- React component `<ChewieChat />` with full TypeScript support
- Headless client `createChewieClient()` for custom implementations
- Vanilla JavaScript embed for non-React sites
- Dual build output (ESM + CJS) with `.d.ts` types
- Mock mode for local development without backend
- Branded dark theme with CSS variables (light theme support)
- i18n support (English & Polish)
- DeFi-optimized UI components:
  - Earnings card with APR display
  - Source citations
  - Follow-up question chips
  - Suggested prompts
- Accessibility features:
  - WCAG 2.1 AA compliant
  - Keyboard navigation
  - Focus trap in modal
  - Screen reader support
  - `prefers-reduced-motion` support
- Event system for analytics tracking
- Session management with UUID persistence
- Comprehensive test suite (Vitest + jest-axe)
- React and vanilla JavaScript examples
- Production-ready documentation

### Technical

- Built with TypeScript, React 18, tsup
- CSS Modules for encapsulated styles
- Zero external runtime dependencies (React/ReactDOM are peer deps)
- Tree-shakeable with `sideEffects: false`
- Bundle size: ~35KB min+gz (excluding React)

## [Unreleased]

### Planned

- Additional languages (Spanish, French, German)
- Theme builder/customizer
- Streaming responses
- File upload support
- Voice input
- Widget analytics dashboard
