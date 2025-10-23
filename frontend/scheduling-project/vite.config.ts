import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://api:8000',  // 'api' is the Docker service name
        changeOrigin: true,
        rewrite: (p) => p,          // keep the /api prefix
      },
    },
  },
})
