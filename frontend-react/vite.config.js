import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig(({ mode }) => {
  // Явное указание местоположения файла с переменными окружения в директории выше
  const envDir = path.resolve(__dirname, '..');
  //
  // Получение переменных окружения из файла
  const env = loadEnv(mode, envDir, '') // '' - Означает загрузку всех префиксов
  //
  console.log('VITE_MAIN_BACK_SERVER_PATH is: ', env.VITE_MAIN_BACK_SERVER_PATH)
  //
  return {
    plugins: [react()],
    //
    // Указание где искать переменные окружения
    envDir: '../',
    //
    server: {
      proxy: {
        // Сейчас по факту не используется
        '/api': {
          target: 'http://127.0.0.1:8000/',
          changeOrigin: true,

          
          rewrite: (path) => path.replace('/api', ''),
        }
      }
    }
  }
})