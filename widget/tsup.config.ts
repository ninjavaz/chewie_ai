import { defineConfig } from 'tsup';

export default defineConfig([
  // Main library builds (ESM + CJS)
  {
    entry: {
      index: 'src/index.ts',
    },
    format: ['esm', 'cjs'],
    dts: true,
    splitting: false,
    sourcemap: true,
    clean: true,
    external: ['react', 'react-dom'],
    minify: true,
    treeshake: true,
    loader: {
      '.css': 'local-css',
    },
    esbuildOptions(options, context) {
      if (context.format === 'esm') {
        options.banner = {
          js: '"use client";',
        };
      }
    },
  },
  // Vanilla JS builds (ESM + CJS)
  {
    entry: {
      vanilla: 'src/vanilla.ts',
    },
    format: ['esm', 'cjs'],
    dts: true,
    splitting: false,
    sourcemap: true,
    external: ['react', 'react-dom'],
    minify: true,
    treeshake: true,
    loader: {
      '.css': 'local-css',
    },
  },
  // Browser IIFE build (bundles everything)
  {
    entry: {
      'vanilla.browser': 'src/vanilla.ts',
    },
    format: ['iife'],
    globalName: 'ChewieChat',
    splitting: false,
    sourcemap: true,
    minify: true,
    treeshake: true,
    loader: {
      '.css': 'local-css',
    },
    noExternal: ['react', 'react-dom'],
    esbuildOptions(options) {
      options.footer = {
        js: 'if(typeof window!=="undefined"){window.ChewieChat=ChewieChat;}',
      };
    },
  },
]);
