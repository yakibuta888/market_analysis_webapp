/// <reference types="vitest" />
import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react-swc";
import dynamicImport from "vite-plugin-dynamic-import";
import checker from 'vite-plugin-checker';
import path, { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const apiUrl = env.VITE_API_URL || 'http://backend:8000';

  return {
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
          target: apiUrl,
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
    build: {
      outDir: 'dist',
      assetsDir: 'assets',
      rollupOptions: {
        output: {
          manualChunks: undefined,
        },
      },
    },
    base: '/', // 本番環境のベース URL に合わせて修正
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
      coverage: {
        provider: 'v8',
        reporter: ['text', 'json-summary', 'json'],
        reportOnFailure: true,
      },
    },
  }
});
