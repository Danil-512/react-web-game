import { setVariavle, exitVariables} from '../sessionlVariables.js'
import { f_Check_CSFR_For_Post_Request, f_Get_CSRF_Token_From_Cookie, f_Send_Post_Request, f_Send_Get_Request } from './csfr_functions.js'

export const backServerPath = import.meta.env.VITE_MAIN_BACK_SERVER_PATH;

// axios.defaults.xsrfCookieName = 'csrftoken';
// axios.defaults.xsrfHeaderName = 'X-CSRFToken';
// axios.defaults.withCredentials = true;  // Все запросы будут с куками

// csrf токен получается при первом get запросе на бэк и хранится в куках браузера.
// При каждом post запросе должен отправляться csfr токен для определения подленности пользователя
// Пользователь может первой открыть любую страницу и отправить любой запрос, поэтому в случае отсутствия токена, его нужно получить



export const postNewArticle_1 = async (p_lawId, p_postData) => {
  const response = await f_Send_Post_Request(
    `${backServerPath}/laws/${p_lawId}/newArticle/`,
    p_postData
  );
  //
  return response;
}
// Добавление статьи с проверкой csfr токена
/**
  * Функция для создания новой статьи закона.
  * @param   { number }     p_lawId - Ид закона.
  * @param   { p_postData } p_postData - Данные новой статьи (JSON) - {
      article_title: 'Название статьи',
      points: ['Текст первого пункта', 'Текст второго пункта', 'Текст третьего пункта'],
      responsibilities: {
        criminal: false/true,
        administrative: false/true,
        civil: false/true,
        other: false/true
      }
    }.
  * @returns { object }     'server response or { success: true, data: response.data }'.
*/
export const postNewArticle = f_Check_CSFR_For_Post_Request(postNewArticle_1);


// /----------------------------------------------------------------------------------------------------------------------------------------------
// /exitr - post запрос на сервер для выхода из аккаунта
export const postExit = async () => {
  try {
    console.log(`Выход из аккаунта. Начат процесс отправки данных на ${backServerPath}`);
    //
    const postStr = {
      "type": "exit"
      , "data1": "_"
      , "data2": "_"
      , "data3": "_"
    };
    //
    console.log("Exit. Начало отправки");
    //
    exitVariables()
    //
    const response = await f_Send_Post_Request(
      `${backServerPath}/`, 
      postStr
    );
    //
    return response.data === "ExitOK" 
      ? "ExitOK" 
      : "ExitNOTOK";
  }
  catch {
    console.log("Ошибка выхода из аккаунта.")
  }
}

// /----------------------------------------------------------------------------------------------------------------------------------------------
// /postRegister - post запрос на сервер для регистрации пользователя
const postRegister_1 = async (login, password) => {
  try {
    console.log("Backend path:", backServerPath);
    printSessionInfo();
    //
    // Создание переменной с отправляемыми данными
    const postStr = {
      "userLogin":    `${login}`,
      "userPassword": `${password}`,
    }
    //
    // Основной запрос на регистрацию
    const response = await f_Send_Post_Request(
      `${backServerPath}/reg/`,
      postStr
    );
    //
    printSessionInfo();
    //
    // Регистрация прошла успешно
    console.log('return { success: true, data: response.data };');
    return { success: true, data: response.data };
  } catch (error) {
    console.error("Register error:", error);
  }
};
// postRegister - post запрос на сервер для регистрации пользователя/
// ----------------------------------------------------------------------------------------------------------------------------------------------/
//
// Регистрация с проверкой csfr токена
export const postRegister = f_Check_CSFR_For_Post_Request(postRegister_1);



// /----------------------------------------------------------------------------------------------------------------------------------------------
// /postAuthorization - post запрос на сервер для авторизации пользователя
export const postAuthorization_1 = async (login, password) => {
  try {
    printSessionInfo();
    //
    console.log(`Авторизация. Начат процесс отправки данных на ${backServerPath}`);
    //
    // Создание переменной с отправляемыми данными
    const postStr = {
      "userLogin":    `${login}`,
      "userPassword": `${password}`,
    }
    //
    console.log("Авторизация. Начало отправки")
    //
    // Отправление запроса на авторизацию и получение ответа в переменную response
    const response = await f_Send_Post_Request(
      `${backServerPath}/auth/`,
      postStr
    ); 
    //
    // После успешной авторизации проверьте сессию
    const sessionCheck = await f_Send_Get_Request(`${backServerPath}/check-session/`);
    //
    // Вывод полученной информации о сессии - понадобиться при настройке сессий
    console.log('Session check:', sessionCheck.data);
    console.log(`Response in function.js is: ${response.data.message}`);
    //
    // ЗАЧЕМ ОНО НАДО
    setVariavle('session_user_login', login);
    setVariavle('session_user_access_level', response.data.access_type);
    //
    printSessionInfo();
    //
    // Авторизация прошла успешно
    return { success: true, data: response.data.message };
  } catch (err) {
    console.error(`Ошибка авторизации пользователя: ${err}`);
  }
}
// postAuthorization/
// ----------------------------------------------------------------------------------------------------------------------------------------------/
//
// Авторизация с проверкой csfr токена
export const postAuthorization = f_Check_CSFR_For_Post_Request(postAuthorization_1);



// Функция для вывода информации о сессии и куках
export const printSessionInfo = () => {
  // Выводим все куки
  //console.log('Все куки:', document.cookie);
  //
  // Выводим конкретно sessionid и csrftoken
  const cookies = document.cookie.split('; ').reduce((prev, current) => {
    const [name, value] = current.split('=');
    prev[name] = value;
    return prev;
  }, {});
  //
  console.log('Session ID:', cookies['sessionid'] || 'Не найден');
  console.log('CSRF Token:', cookies['csrftoken'] || 'Не найден');
};