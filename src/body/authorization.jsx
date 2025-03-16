import React, { useState, useEffect, useRef } from 'react';
import './body.css'
import { getData, postAuthorization } from '../front_functions/functions.js'

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
function authorization() {
    // Состояния объектов 
    const [datas, setDatas] = useState({ details: [], })
    const [login, setLogin] = useState("");
    const [password, setPassword] = useState("");
    const [status, setStatus] = useState("");

    // Ссылка на логин
    const inputRefLogin = useRef(null);
    // Ссылка на пароль
    const inputRefPassword = useRef(null);

    // const [back, setBack] = useState("");
    // const [back1, setBack1] = useState({
    //     value1: 1,
    //     value2: 2,
    //     value3: 3
    // });
    // // Обращение - back1.value1
    // const [back2, setBack2] = useState(() => {
    //     const initialState = function () {
    //         return 0;
    //     }()
    //     return initialState;
    // });

    // Хук useEffect позволяет выполнять побочные эффекты в функциональном компоненте 
    // Данный хук позволяет выполнять некоторый кот в те моменты, когда компонент рендрится и ререндриться,
    //  или пропадает с экрана, или когда изменяется одна из зависимых переменных

    
    // export const UseEffectExample = () => {
    //     useEffect(() => {
    //         console.log("Рендр компонента")
    //         return 
    //     }
    // }, [])
    
    // /-------------------------------------------------------------------------------------------------------
    // /Функция обновления данных в инпуте с паролем
    const handlePasswordChange = (event) => {
        // console.log(`-----------------------------------------`)
        // console.log(`Событие на странице: handlePasswordChange`)
        //setPassword(event.target.value);
    };
    // Функция обновления данных в инпуте с паролем/
    // -------------------------------------------------------------------------------------------------------/

    // /-------------------------------------------------------------------------------------------------------
    // /Функция нажатия кнопки на странице авторизации
    const handleButtonClick = () => {
        console.log(`-----------------------------------------`)
        console.log(`Событие на странице: handleLoginClick`)

        // /Получение данных от бэкенда
        //getData(backServerPath, datas, setDatas);
        // Получение данных от бэкенда/

        // /Переменные с паролем и логином
        const login = inputRefLogin.current.value;
        const password = inputRefPassword.current.value;
        console.log(`---Password is: ${password}, Login is: ${login}.`)
        // Переменные с паролем и логином/

        // /Отправка данных серверу
        postAuthorization(backServerPath, login, password);
        // Отправка данных серверу/


        //setData(MyComponent());
        setStatus("Контакт с сервером установлен");

        // Здесь можно добавить логику для обновления логина на основе пароля
        //setLogin(password); // Пример: обновляем логин значением из поля пароля
    };
    // Функция нажатия кнопки на странице авторизации/
    // -------------------------------------------------------------------------------------------------------/


    // /-------------------------------------------------------------------------------------------------------
    // /Возвращаемая верстка
    return (
        <div class="authorization" id='div1' key='div1'>
            <p className="auth1">Авторизация пользователя</p>
            
            <p className="auth1">Логин</p>
            <input className="auth1" id='login' ref={inputRefLogin}></input>

            <p className="auth1">Пароль</p>
            <input className="auth1" id='password' ref={inputRefPassword} onChange={handlePasswordChange}></input>
                    
            <p>
                <button /*type='submit'*/ className="auth1" id='button1' onClick={handleButtonClick}>
                    Войти
                </button>
            </p>

            <p>
                {status}
            </p>
        </div>
    )
    // Возвращаемая верстка/
    // -------------------------------------------------------------------------------------------------------/
}
// Возвращаемая функция/
// ----------------------------------------------------------------------------------------------------------------------------------------------/


export default authorization;