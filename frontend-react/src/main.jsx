import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
// Библиотека для работы с http запрсами
import axios from 'axios'




// Функция для рендера ВСЕГО
function allRender() {
    const root = document.getElementById('root');

    // Точка входа в приложение
    createRoot(root).render(<App />)
}

// Первый рендер страницы
allRender();
