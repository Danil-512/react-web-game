import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './body.css'


// Получение данных от джанго
const componentDidMount = () => {
    let data = [];

    axios.get('http://localhost:8000/')
    .then(res => {data = res.data;})
    .catch(err => {console.log(err);})
    ;

    return data;
}



function authorization() {
    // Состояния объектов 
    const [login, setLogin] = useState("");
    const [password, setPassword] = useState("");
    const [data, setData] = useState("");
    const [back, setBack] = useState("");

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleLoginClick = () => {
        // Здесь можно добавить логику для обновления логина на основе пароля
        setLogin(password); // Пример: обновляем логин значением из поля пароля
    };

    return (<div class="authorization" id='div1' key='div1'>
                <p className="auth1">Авторизация пользователя</p>
                
                <p className="auth1">Логин</p>
                <input className="auth1" id='login'value={login}></input>
                <p className="auth1">Пароль</p>
                <input className="auth1" id='password' onChange={handlePasswordChange}>
                </input>
            
                <p>
                    <button /*type='submit'*/ className="auth1" id='button1' onClick={handleLoginClick}>
                        Войти
                    </button> 
                </p>
            </div>
            )
}


export default authorization;