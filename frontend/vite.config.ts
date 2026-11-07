import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// 배포 시 404.semo3.com/app 아래에서 동작한다. 개발 중 /api 요청은 로컬 백엔드로 넘긴다.
export default defineConfig({
  base: '/app/',
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
})
