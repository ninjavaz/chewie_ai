import { defineConfig } from 'tsup';

export default defineConfig({
  entry: {
    index: 'src/index.ts',
    vanilla: 'src/vanilla.ts',
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
  esbuildOptions(options) {
    options.banner = {
      js: '"use client";',
    };
  },
});
