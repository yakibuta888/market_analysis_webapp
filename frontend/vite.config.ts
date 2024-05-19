/// <reference types="vitest" />
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import dynamicImport from "vite-plugin-dynamic-import";
import checker from 'vite-plugin-checker';
import path, { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig({
  // プラグイン React, Dynamic Import
  plugins: [
    react(),
    dynamicImport(),
    checker({ typescript: true })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    // 使用するポート番号の指定 default 3000
    port: 3001,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        configure: (proxy, options) => {
          // proxy は 'http-proxy' のインスタンスです
          proxy.on('proxyReq', function (proxyReq, req, res) {
            console.log('Proxying request to: ', req.url);
          });
        },
      }
    }
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
    setupFiles: [resolve(__dirname, "src", "vitest-setup.ts")],
  },
});
