import React, { useState, useEffect, useRef } from 'react';
import './body.css'
import { getData, postAuthorization, postRegister    } from '../front_functions/functions.js'
import { useNavigate } from 'react-router-dom';

// Адрес бэкенд сервера: 
const backServerPath = 'http://127.0.0.1:8000/';

// ----------------------------------------------------------------------------------------------------------------------------------------------/
// /Примеры работы функций для общения с сервером

// // /Получение данных от бэкенда - получение списка данных на стандартный get запрос
// getData(backServerPath, datas, setDatas);
// // Получение данных от бэкенда/

// Примеры работы функций для общения с сервером/
// ----------------------------------------------------------------------------------------------------------------------------------------------/


// ----------------------------------------------------------------------------------------------------------------------------------------------/
// /Возвращаемая функция
function register() {
    // Ссылка на логин
    const inputRefLogin = useRef(null);
    // Ссылка на пароль
    const inputRefPassword = useRef(null);

    const handleButtonClick = async () => {
        console.log(`-----------------------------------------`)
        console.log(`Событие на странице: handleLoginClick - Register`)
        // /Переменные с паролем и логином
        const login = inputRefLogin.current.value;
        const password = inputRefPassword.current.value;
        console.log(`---Password is: ${password}, Login is: ${login}.`)
        await postRegister(login, password)
                .then(function (response) {
                    console.log("2");
                    console.log(`Login: ${inputRefLogin}, Password: ${inputRefPassword}`);
                    console.log(`Status: ${response}`)
                    if (response === "RegisterOK") {
                        console.log("Регистрация прошла, должен был произойти переход1")
            
                        navigate('/main');
                        console.log("Регистрация прошла, должен был произойти переход2")
                    }
                    else {
                        console.log('Неудачная регистрация');
                    }
                });;
    };

    

    
    
    return (
        <div className='authorization'>
            <p className="auth1">Регистрация пользователя</p>
            
            <p className="auth1">Логин</p>
            <input className="auth1" id='login' ref={inputRefLogin}></input>

            <p className="auth1">Пароль</p>
            <input className="auth1" id='password' ref={inputRefPassword}></input>
            <p className="auth1"></p>
            <button onClick={handleButtonClick}>Зарегистрироваться</button>
        </div>
    )
}

export default register