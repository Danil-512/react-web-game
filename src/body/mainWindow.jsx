import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './body.css';
const backServerPath = 'http://127.0.0.1:8000/';

function MainWindow() {
    const navigate = useNavigate();

    const handleButtonLawsClick = async () => {
        console.log(`-----------------------------------------`)
        console.log(`Событие на странице: handleLoginClick - Laws`)
        navigate('/laws');
    }

    return (
        <div className="main_menu_all">
            <h1>Главная страница</h1>
            <div className='buttons-div'>
                <div className='main_menu_el'>
                    <button className='main_menu_button' onClick={handleButtonLawsClick}>
                        Законодательство
                    </button>
                </div>
            </div>
        </div>
  );
}

export default MainWindow;