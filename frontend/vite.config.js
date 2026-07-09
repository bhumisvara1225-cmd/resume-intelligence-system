import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
      }
    }
  },
  build: {
    outDir: '../app/static',
    emptyOutDir: true,
  },
  define: {
    // Expose VITE_API_URL to the frontend (set in Vercel environment variables)
    __API_URL__: JSON.stringify(process.env.VITE_API_URL || ''),
  }
}))
