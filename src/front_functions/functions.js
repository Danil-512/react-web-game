import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getVariables, setVariavle, exitVariables} from '../sessionlVariables.js'


const backServerPath = 'http://localhost:8000/';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;  // Все запросы будут с куками

// /----------------------------------------------------------------------------------------------------------------------------------------------
// /getData - get запрос на сервер для получения списка json данных
export const getData = async (datas, setDatas) => {
    let answer;
    let answers = [];
    try {
      // Начинаем процесс загрузки
        console.log(`Начат процесс получения данных от ${backServerPath}`);


      // /-------------------------------------------------------------------------------------------------------
      // /axios get
        //await axios.get('http://127.0.0.1:8000/')
        await axios.get(backServerPath, {
          withCredentials: true,
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
          }
        })
        .then(response => {
            console.log(`response.data[0] is: ${response.data[0].title}: ${response.data[0].content}`)
            setDatas({
                // В состояние datas, которое хранит объект, единственным элементом которого является пара ключ-значение 
                // ключ - details, значение - массив 
                details: response.data
                // Теперь надо узнать, что это. Я думаю, что это массив со строками, где каждая строка - хранимый json/
                // Как теперь пройтись по этому массиву? Если это конечно массив
            });                
            console.log(`axios: Данные получены от ${backServerPath} получены.`)
        })
        .catch(err => {
            console.log(`axios: Ошибка получения данных от сервера: ${err}.`);
        })
        ;
      // axios get/
      // -------------------------------------------------------------------------------------------------------/

      
      // /-------------------------------------------------------------------------------------------------------
      // /Работа с полученным от axios массивом
      // Метода map позволяет трансформировать один массив в друго, последовательно обращаясь к каждому элементу
      // тут он используется для перебора значение массива details
      console.log(`Вывод данных из datas.details:`)
      datas.details.map((el) => {
        console.log(`details: response.data is: ${el.title}`)
      })
      // Этот метод для перебора значений тоже работает
      for (let item of datas.details) {
        console.log(`item.content is: ${item.title}`)
      }
      // И этот тоже...
      datas.details.forEach(element => {
        console.log(`datas.details.forEach is: ${element.title}`)
      });
      // Работа с полученным от axios массивом/
      // -------------------------------------------------------------------------------------------------------/
    } catch (e) {
      console.log(e);
    }
}
// getData/
// ----------------------------------------------------------------------------------------------------------------------------------------------/

// /----------------------------------------------------------------------------------------------------------------------------------------------
// /exitr - post запрос на сервер для выхода из аккаунта
export const postExit = async () => {
  try {
    console.log(`Выход из аккаунта. Начат процесс отправки данных на ${backServerPath}`);
    const postStr = {
      "type": "exit"
      , "data1": "_"
      , "data2": "_"
      , "data3": "_"
    };
    //
    // /-------------------------------------------------------------------------------------------------------
      // /axios post
      console.log("Exit. Начало отправки");
      exitVariables()
      let status1 = "ExitNOTOK";
      const response = await axios.post(backServerPath, postStr, {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        }
      }); 
      return response.data === "ExitOK" 
          ? "ExitOK" 
          : "ExitNOTOK";
    // axios post/
    // -------------------------------------------------------------------------------------------------------/
  }
  catch {
    console.log("Ошибка выхода из аккаунта.")
  }
}

// /----------------------------------------------------------------------------------------------------------------------------------------------
// /postRegister - post запрос на сервер для регистрации пользователя
export const postRegister = async (login, password) => {
  try {
    printSessionInfo();
    // 1. Сначала делаем GET запрос для получения CSRF токена
    const csrfResponse = await axios.get('http://localhost:8000/get-csrf/', {
      withCredentials: true
    });

    // 2. Получаем CSRF токен из кук
    const getCSRFToken = () => {
      const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
      return cookieValue || '';
    };

    const csrfToken = getCSRFToken();

    // 3. Основной запрос на регистрацию
    const response = await axios.post(
      'http://localhost:8000/',
      {
        type: "register",
        data1: login,
        data2: password,
        data3: "_"
      }, 
      {
        withCredentials: true,  // Важно!
        headers: {
          'X-CSRFToken': getCSRFToken(),
          'Content-Type': 'application/json'
        }
      }
    );
    printSessionInfo();
    return response.data;
  } catch (error) {
    console.error("Register error:", error);
    throw error;
  }
};
// postRegister - post запрос на сервер для регистрации пользователя/
// ----------------------------------------------------------------------------------------------------------------------------------------------/


// /----------------------------------------------------------------------------------------------------------------------------------------------
// /postAuthorization - post запрос на сервер для авторизации пользователя
export const postAuthorization = async (login, password) => {
    try {
      printSessionInfo();
      // Начинаем процесс отправки
        console.log(`Авторизация. Начат процесс отправки данных на ${backServerPath}`);
        //const postStr = {`"type": ${login}, ""content"": ${password}`}
        const postStr = {
          "type": "authorization"
          , "data1": `${login}`
          , "data2": `${password}`
          , "data3": "_"
        }
        

      // /-------------------------------------------------------------------------------------------------------
      // /axios post
        //await axios.post('http://127.0.0.1:8000/')
        console.log("Авторизация. Начало отправки")
        checkSession();
        let status1 = "AuthorizationNOTOK"
        // Почему авторизация Post? Нужен ведь Get
        // Сюда добавляю отправление кук на сервер
        const response = await axios.post(backServerPath, postStr, {
          withCredentials: true,  // Важно!
          headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
          }
        }); 

        // После успешной авторизации проверьте сессию
        const sessionCheck = await axios.get('http://localhost:8000/check-session/', {
            withCredentials: true
        });

        console.log('Session check:', sessionCheck.data);

        console.log(`Response in function.js is: ${response.data.split('-')[0]}`);

        console.log(`response.data.split('-')[1] is: ${response.data.split('-')[1]}`);

        setVariavle('session_user_login', login);
        setVariavle('session_user_access_level', response.data.split('-')[1]);
        printSessionInfo();
        checkSession();
        return response.data.split('-')[0] === "AuthorizationOK" 
            ? "AuthorizationOK" 
            : "AuthorizationNOTOK";
      // axios post/
      // -------------------------------------------------------------------------------------------------------/
    } catch (err) {
        console.log(`axios: Ошибка отправки данных серверу: ${err}.`);
    }
}
// postAuthorization/
// ----------------------------------------------------------------------------------------------------------------------------------------------/

// Функция для получения CSRF-токена из кук
const getCSRFToken = () => {
    const cookieValue = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
};

// Функция для вывода информации о сессии и куках
export const printSessionInfo = () => {
  // Выводим все куки
  //console.log('Все куки:', document.cookie);
  
  // Выводим конкретно sessionid и csrftoken
  const cookies = document.cookie.split('; ').reduce((prev, current) => {
    const [name, value] = current.split('=');
    prev[name] = value;
    return prev;
  }, {});

  console.log('Session ID:', cookies['sessionid'] || 'Не найден');
  console.log('CSRF Token:', cookies['csrftoken'] || 'Не найден');
  
  // Можно также вывести localStorage/sessionStorage
  //console.log('localStorage:', localStorage);
  //console.log('sessionStorage:', sessionStorage);
};

// После успешной авторизации сделайте тестовый запрос для проверки сессии
const checkSession = async () => {
  try {
    const response = await axios.get('http://localhost:8000/', {
      withCredentials: true,
      headers: {
        'X-CSRFToken': getCSRFToken()
      }
    });
    console.log('Session check:', response.headers);
  } catch (error) {
    console.error('Session check failed:', error);
  }
}