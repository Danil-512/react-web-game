import axios from 'axios';
import { setVariavle, exitVariables} from '../sessionlVariables.js'


export const backServerPath = import.meta.env.VITE_MAIN_BACK_SERVER_PATH;

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;  // Все запросы будут с куками

// /----------------------------------------------------------------------------------------------------------------------------------------------
// /getData - get запрос на сервер для получения списка json данных
export const getData = async (datas, setDatas) => {
  try {
    console.log(`Начат процесс получения данных от ${backServerPath}`);
    //
    await axios.get(`${backServerPath}/`, {
      withCredentials: true,
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      }
    })
    .then(response => {
      console.log(`response.data[0] is: ${response.data[0].title}: ${response.data[0].content}`)
      setDatas({details: response.data});                
      console.log(`axios: Данные получены от ${backServerPath} получены.`)
    })
    .catch(err => {
      console.log(`axios: Ошибка получения данных от сервера: ${err}.`);
    });
    //
    // Метод map позволяет трансформировать один массив в друго, последовательно обращаясь к каждому элементу
    // тут он используется для перебора значение массива details
    console.log(`Вывод данных из datas.details:`)
    datas.details.forEach(element => {
      console.log(`datas.details.forEach is: ${element.title}`)
    });
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
    const response = await axios.post(`${backServerPath}/`, postStr, {
      withCredentials: true,
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      }
    });
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
export const postRegister = async (login, password) => {
  try {
    console.log("Backend path:", backServerPath);
    printSessionInfo();
    //
    // 2. Получаем CSRF токен из кук
    const getCSRFToken = () => {
      const cookieValue = document.cookie
                                  .split('; ')
                                  .find(row => row.startsWith('csrftoken='))
                                  ?.split('=')[1];
      return cookieValue || '';
    };
    //
    // Создание переменной с отправляемыми данными
    const postStr = {
      "userLogin":    `${login}`,
      "userPassword": `${password}`,
    }
    //
    // 3. Основной запрос на регистрацию
    const response = await axios.post(
      `${backServerPath}/reg/`,
      postStr, 
      {
        withCredentials: true,  // Важно!
        headers: {
          'X-CSRFToken': getCSRFToken(),
          'Content-Type': 'application/json'
        }
      }
    );
    //
    printSessionInfo();
    //
    // Регистрация прошла успешно
    return { success: true, data: response.data };
  } catch (error) {
    console.error("Register error:", error);
    //
    // Если получен ответ - значит ошибка со стороны бэка
    if (error.response) {
      const status       = error.response.status;
      //
      if (status == 400) {
        console.error('Ошибка регистрации! Некорректные данные.');
        return { success: false, error: `Неккорректные данные!` };
      }
      else if (status == 500) {
        console.error('Ошибка регистрации! Ошибка в работе бэка.');
        return { success: false, error: `Ошибка в работе бэка!` };
      }
    } 
    // Если нет, значит до бэка запрос не дошел
    else {
      return { success: false, error: 'Ошибка при подключении к бэку!' };
    }
    //throw error;
  }
};
// postRegister - post запрос на сервер для регистрации пользователя/
// ----------------------------------------------------------------------------------------------------------------------------------------------/


// /----------------------------------------------------------------------------------------------------------------------------------------------
// /postAuthorization - post запрос на сервер для авторизации пользователя
export const postAuthorization = async (login, password) => {
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
    checkSession();
    //
    // Отправление запроса на авторизацию и получение ответа в переменную response
    const response = await axios.post(
      `${backServerPath}/auth/`,
      postStr,
      {
        withCredentials: true,  // Важно!
        headers: {
          'X-CSRFToken': getCSRFToken(),
          'Content-Type': 'application/json'
        }
      }
    ); 
    //
    // После успешной авторизации проверьте сессию
    const sessionCheck = await axios.get(
      `${backServerPath}/check-session/`, 
      {
        withCredentials: true
      }
    );
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
    checkSession();
    //
    // Авторизация прошла успешно
    return { success: true, data: response.data.message };
  } catch (err) {
    console.log(`Ошибка авторизации пользователя: ${err}`);
    //
    // Если получен ответ - значит ошибка со стороны бэка
    if (error.response) {
      const status       = error.response.status;
      //
      if (status == 401) {
        console.error('Ошибка авторизации! Некорректные данные.');
        return { success: false, error: `Неверный логин или паролье!` };
      }
      else if (status == 500) {
        console.error('Ошибка авторизации! Ошибка в работе бэка.');
        return { success: false, error: `Ошибка в работе бэка!` };
      }
    } 
    // Если нет, значит до бэка запрос не дошел
    else {
      return { success: false, error: 'Ошибка при подключении к бэку!' };
    }
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

// После успешной авторизации сделайте тестовый запрос для проверки сессии
const checkSession = async () => {
  try {
    const response = await axios.get(
      `${backServerPath}/`,
      {
        withCredentials: true,
        headers: {
          'X-CSRFToken': getCSRFToken()
        }
      }
    );
    console.log('Session check:', response.headers);
  } catch (error) {
    console.error('Session check failed:', error);
  }
}