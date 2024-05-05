import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import dynamicImport from "vite-plugin-dynamic-import";
import checker from 'vite-plugin-checker';
import { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig({
  // プラグイン React, Dynamic Import
  plugins: [
    react(),
    dynamicImport(),
    checker({ typescript: true })
  ],
  server: {
    // 使用するポート番号の指定 default 3000
    port: 3001,
  },
  // テスト参考
  // https://vitest.dev/guide/#workspaces-support
  // https://testing-library.com/docs/svelte-testing-library/setup/
  test: {
    //  describe, expect, it などのAPIをファイル内でimportしなくても使用可にする設定
    globals: true,
    // dom
    environment: "happy-dom",
    // テスト全体で使用するライブラリをvitest-setup.jsに記載し、インポートする設定
    setupFiles: [resolve(__dirname, "src", "vitest-setup.js")],
  },
});
