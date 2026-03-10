import { defineConfig } from "vite";
import { resolve } from "node:path";

export default defineConfig({
  build: {
    lib: {
      entry: resolve(__dirname, "src/katex-init.ts"),
      name: "KatexInit",
      formats: ["iife"],
      fileName: "katex-init",
    },
    rollupOptions: {
      external: ["katex"],
      output: {
        globals: {
          katex: "katex",
        },
      },
    },
    emptyOutDir: true,
  },
});
