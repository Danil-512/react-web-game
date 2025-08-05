import { createRoot } from 'react-dom/client'

import App from './App.jsx'

import './index.css'


// Функция для рендера ВСЕГО
function allRender() {
  const root = document.getElementById('root');
  //
  // Точка входа в приложение
  createRoot(root).render(<App />)
}

// Первый рендер страницы
allRender();