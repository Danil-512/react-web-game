import axios from 'axios';
import { backServerPath } from './functions.js'


/**
  * Отправляет post запрос на сервер с добавлением нужных токенов.
  * @param {string} p_Server_Path - Адрес сервера получателя.
  * @param {string} p_Post_Data - Текст отправляемого запроса (JSON).
  * @returns { object } 'server response or { success: true, data: response.data }'.
*/
export async function f_Send_Post_Request(p_Server_Path, p_Post_Data) {
  const c_CSFR_Token    = f_Get_CSRF_Token_From_Cookie();
  //
  // Проверка полученного токена
  if (!c_CSFR_Token) {
    return {success: false, error: `The required CSFR token is missing!`}
  }
  //
  // Попытка отправления post запроса на бэк сервер
  try {
    const response = await axios.post(
      p_Server_Path,
      p_Post_Data,
      {
        withCredentials: true,
        headers: {
          'X-CSRFToken': c_CSFR_Token,
          'Content-Type': 'application/json'
        },
        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFToken',
      }
    );
    //
    return {success: true, data: response.data };
  } catch (error) {
    console.error("Error:", error);
    //
    // Если получен ответ - значит ошибка со стороны бэка
    if (error.response) {
      const status = error.response.status;
      //
      if (status == 400) {
        console.error('Ошибка сервера! Некорректные данные.');
        return { success: false, error: `Неккорректные данные!` };
      }
      if (status == 401) {
        console.error('Ошибка сервера! Некорректные данные.');
        return { success: false, error: `Неверный логин или пароль!` };
      }
      else if (status == 500) {
        console.error('Ошибка сервера! Ошибка в работе бэка.');
        return { success: false, error: `Ошибка в работе бэка!` };
      }
    } 
    // Если нет, значит до бэка запрос не дошел
    else {
      return {success: false, error: `axios: Ошибка получения данных от сервера: ${error}.`}
    }
  }
}


/**
  * Отправляет get запрос на сервер с добавлением нужных токенов.
  * @param {string} p_Server_Path - Адрес сервера получателя.
  * @returns { object } 'server response or { success: true, data: response.data }'.
*/
export async function f_Send_Get_Request(p_Server_Path) {
  const c_CSFR_Token = f_Get_CSRF_Token_From_Cookie();
  //
  // Проверка полученного токена
  if (!c_CSFR_Token) {
    return {success: false, error: `The required CSFR token is missing!`}
  }
  //
  // Попытка отправления get запроса на бэк сервер
  try {
    const response = await axios.get(
        p_Server_Path,
        {
          withCredentials: true,
          headers: {
            'X-CSRFToken': c_CSFR_Token,
            'Content-Type': 'application/json'
          },
          xsrfCookieName: 'csrftoken',
          xsrfHeaderName: 'X-CSRFToken',
        }
      );
    //
    return {success: true, data: response.data };
  } catch (error) {
    return {success: false, error: `axios: Ошибка получения данных от сервера: ${error}.`}
  }
}


// Декоратор для проверки наличия csfr токена в куках браузера.
// Если токена нет, вызов функции для его получения
export function f_Check_CSFR_For_Post_Request(targetunction) {
  // Будет возвращена измененная функция с дополнительным функционалом проверки и получения csfr
  return async function (...args) {
    //
    // Получение csfr токена из кук браузера
    let v_Csfr_From_Cookies = f_Get_CSRF_Token_From_Cookie();
    //
    //Проверка наличия токена
    if (!v_Csfr_From_Cookies) {
      console.log('Cookie dont have csfr token. Getting a new token:');
      //
      try {
        // Получение нового csfr токена. Его не надо куда-то присваивать, он автоматически сохранится в куках браузера
        await f_Get_CSRF_Token_From_Back().then(response => {
          v_Csfr_From_Cookies = f_Get_CSRF_Token_From_Cookie();
          //
          if (csfrFromCookies) {
            console.log(`Successful receipt of token: ${v_Csfr_From_Cookies}`);
          } else {
            // Если произошла ошибка при получении токена, вернуть ошибку
            return { success: false, error: `CSRF token not received`}
        }
      })
      } catch (error) {
        console.error(`Error getting token ${error}`);
        return { success: false, error: `Error getting CSFR token ${error}`}
      }
    }
    //
    // Токен успешно получен, можно вызывать оригинальную функцию
    return targetunction.apply(this, args);
  }
}

// Функция для получения CSRF-токена c бэка
export const f_Get_CSRF_Token_From_Back = async () => {
  await axios.get(
    `${backServerPath}/get-csrf/`, 
    {withCredentials: true}
  )
  //
  const csrfToken = document.cookie
                            .split('; ')
                            .find(row => row.startsWith('csrftoken='))
                            ?.split('=')[1];
  //
  console.log(`getCSRFTokenFromBack. Получен токен ${csrfToken}`);
  //
  return csrfToken;
};

// Функция для получения CSRF-токена из кук
export const f_Get_CSRF_Token_From_Cookie = () => {
  const cookieValue = document.cookie
                              .split('; ')
                              .find(row => row.startsWith('csrftoken='))
                              ?.split('=')[1];
  //
  return cookieValue ? cookieValue : '';
};