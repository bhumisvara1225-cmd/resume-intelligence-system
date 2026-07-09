import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [react()],
  server: {
    // Local dev: proxy /api requests to local FastAPI
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
      }
    }
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  }
}))
