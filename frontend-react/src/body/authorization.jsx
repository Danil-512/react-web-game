import { useState, useRef } from 'react';
import './body.css'
import { postAuthorization } from '../front_functions/functions.js'
import { useNavigate } from 'react-router-dom';

// ----------------------------------------------------------------------------------------------------------------------------------------------/
// /Возвращаемая функция
function authorization() {
  // Состояния объектов
  const [status, setStatus] = useState("");
  const navigate = useNavigate();
  //
  // Ссылка на логин
  const inputRefLogin = useRef(null);
  // Ссылка на пароль
  const inputRefPassword = useRef(null);
  //
  // Хук useEffect позволяет выполнять побочные эффекты в функциональном компоненте 
  // Данный хук позволяет выполнять некоторый кот в те моменты, когда компонент рендрится и ререндриться,
  //  или пропадает с экрана, или когда изменяется одна из зависимых переменных
  //
  // /-------------------------------------------------------------------------------------------------------
  // /Функция нажатия кнопки на странице авторизации
  const handleButtonClick = async () => {
    console.log(`-----------------------------------------`)
    console.log(`Событие на странице: handleLoginClick - Authorization`)
    //
    // Переменные с паролем и логином
    const login = inputRefLogin.current.value;
    const password = inputRefPassword.current.value;
    //
    console.log(`---Password is: ${password}, Login is: ${login}.`)
    //
    await postAuthorization(login, password).then(function (response) {
      console.log("2")
      console.log(`Status: ${response.data}`)
      //
      if (response.success) {
        //
        navigate('/main');
        //
        console.log("Авторизация прошла, должен был произойти переход")
        //
        setStatus("Удачная авторизация");
      }
      else {
        setStatus(`Ошибка авторизации ${response.error}`);
      }
    });
  };
  // Функция нажатия кнопки на странице авторизации/
  // -------------------------------------------------------------------------------------------------------/
  //
  // /-------------------------------------------------------------------------------------------------------
  // /Возвращаемая верстка
  return (
    <div className="authorization" id='div1' key='div1'>
      <p className="auth1">Авторизация пользователя</p>

      <p className="auth1">Логин</p>

      <input className="auth1" id='login' ref={inputRefLogin}></input>

      <p className="auth1">Пароль</p>

      <input type="password" className="auth1" id='password' ref={inputRefPassword}></input>

      <button className="auth1" id='button1' onClick={handleButtonClick}>
        Войти
      </button>

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
//export default { session_user_access_level, session_user_access_name, authorization } ;