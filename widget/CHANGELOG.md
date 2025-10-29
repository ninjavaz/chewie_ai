# Changelog

All notable changes to @chewieai/chat-widget will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-01-29

### Added

- 🖱️ **Draggable Modal** - Users can now drag the chat window by clicking and holding the header
- 📏 **Resizable Modal** - Users can resize the chat window from any edge or corner
  - Minimum width: 400px, Maximum width: 800px
  - Minimum height: 400px
  - Resize handles on all 4 edges and 4 corners
- ⬜ **Maximize Button** - Toggle button in header to maximize/restore chat window size
- 🎨 **Avatar Customization** - `avatarUrl` prop now accepts image URLs or emojis
  - Avatar appears in floating button, header, and assistant messages
- 💡 **Engagement Tooltip** - Smart tooltip appears after 2 seconds to encourage interaction
  - Shows "💡 Confused? Let me explain!"
  - Dismisses permanently after first click
  - Customizable via CSS variables
- ✨ **Pulsing Animation** - Floating button has subtle pulse animation to draw attention

### Changed

- 🎨 Updated UI design with modern chat interface
- 👤 Improved message layout with avatars displayed inline
- 🔘 Enhanced floating button with avatar display instead of chat icon
- 📐 Better visual hierarchy and spacing throughout the widget
- 🎯 Improved tooltip positioning and styling

### Fixed

- 🐛 Modal positioning when dragging from left/top edges now works correctly
- 📏 Resize constraints prevent modal from becoming too small or too large
- 🎨 CSS variable consistency across all components

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
