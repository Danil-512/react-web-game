import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const backServerPath = 'http://127.0.0.1:8000/';

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
        await axios.get(backServerPath)
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
      let status1 = "ExitNOTOK";
      const response = await axios.post(backServerPath, postStr); 
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
    console.log(`Регистрация. Начат процесс отправки данных на ${backServerPath}`);
    const postStr = {
      "type": "register"
      , "data1": `${login}`
      , "data2": `${password}`
      , "data3": "_"
    }
    //
    // /-------------------------------------------------------------------------------------------------------
      // /axios post
        console.log("Регистрация. Начало отправки")
        let status1 = "RegisterNOTOK"
        const response = await axios.post(backServerPath, postStr); 
        return response.data === "RegisterOK" 
            ? "RegisterOK" 
            : "RegisterNOTOK";
      // axios post/
      // -------------------------------------------------------------------------------------------------------/
  }
  catch {

  }
}
// postRegister - post запрос на сервер для регистрации пользователя/
// ----------------------------------------------------------------------------------------------------------------------------------------------/


// /----------------------------------------------------------------------------------------------------------------------------------------------
// /postAuthorization - post запрос на сервер для авторизации пользователя
export const postAuthorization = async (login, password) => {
    try {
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
        let status1 = "AuthorizationNOTOK"
        // Почему авторизация Post? Нужен ведь Get
        const response = await axios.post(backServerPath, postStr); 
        //const response = await axios.get(backServerPath, postStr);

        return response.data === "AuthorizationOK" 
            ? "AuthorizationOK" 
            : "AuthorizationNOTOK";


        // .then(function (response) {
        //   console.log(`response.data IS ${response.data}`);
        //   // ТУТ НУЖНО СДЕЛАТЬ, ЧТО ЕСЛИ ОТВЕТ ОТ СЕРВЕРА AuthorizationOK, ТО ИЗМЕНЕНИЕ АКТИВНОГО КОМПОНЕНТА В BODY1.JSX
        //   console.log("Отправляю AuthorizationOK")
        //   return Promise.resolve("AuthorizationOK");
        // })
        // .catch(function (error) {
        //   console.log(error);
        //   return Promise.resolve("AuthorizationNOTOK")
        // })
        // ;
        //console.log(`Server return to post: ${response.data.title}`);
        
      // axios post/
      // -------------------------------------------------------------------------------------------------------/

      
    } catch (err) {
        console.log(`axios: Ошибка отправки данных серверу: ${err}.`);
    }
}
// postAuthorization/
// ----------------------------------------------------------------------------------------------------------------------------------------------/


