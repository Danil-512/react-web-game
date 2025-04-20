import './body.css'
import Authorization from './authorization.jsx'
import Register from './register.jsx'
import MainWindow from './mainWindow.jsx';
import { createBrowserRouter,  BrowserRouter as Router, Routes, Route, Link, useNavigate } from "react-router-dom";

import { NavLink, Outlet } from "react-router"
// <Switch> - Позволяет выбрать первый попавшийся маршрут и использовать его для обработки
//<Authorization />

function body1() {
    return (
        <div className="bodyAll">
            <Outlet />
        </div>
    )
}

// 
export default body1

