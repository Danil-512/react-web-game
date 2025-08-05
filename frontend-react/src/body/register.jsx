import { useState, useRef } from 'react';
import { postRegister } from '../front_functions/functions.js'
import { useNavigate } from 'react-router-dom';

import './body.css'


// ----------------------------------------------------------------------------------------------------------------------------------------------/
// /Возвращаемая функция
function register() {
  // 
  const navigate = useNavigate();
  //
  /// Ссылки на логин и пароль
  const inputRefLogin = useRef(null);
  const inputRefPassword = useRef(null);
  //
  const [status, setStatus] = useState("");    
  //
  const handleButtonClick = async () => {
    console.log(`-----------------------------------------`);
    console.log(`Событие на странице: handleLoginClick - Register`);
    //
    // Переменные с паролем и логином
    const login = inputRefLogin.current.value;
    const password = inputRefPassword.current.value;
    //
    // Вызов функции регистрации из файла functions.js
    await postRegister(login, password).then(function (response) {
      //
      console.log(`Status: ${response}`);
      //
      // Анализ ответа и выполнение действий в зависимости от статуса ответа
      if (response.success) {
        setStatus(`Новый пользователь зарегестрирован: ${inputRefLogin}`)
        //
        navigate('/auth');
        //
        console.log("Регистрация прошла, должен был произойти переход")
      }
      else {
        console.log(`Неудачная регистрация! ${response.error}`);
        //
        setStatus(`Неудачная регистрация: ${response.error}`)
      }
    });
  };
  //
  return (
    <div className='authorization'>
      <p className="auth3">Регистрация пользователя</p>

      <p className="auth1">Логин</p>

      <input className="auth2" id='login' ref={inputRefLogin}></input>

      <p className="auth1">Пароль</p>

      <input type="password" className="auth2" id='password' ref={inputRefPassword}></input>

      <button className="auth1" onClick={handleButtonClick}>Зарегистрироваться</button>

      <p className="auth1">{status}</p>
    </div>
  )
}

export default register