import axios from 'axios';
import { backServerPath } from './functions.js'

// Декоратор для проверки наличия csfr токена в куках браузера.
// Если токена нет, вызов функции для его получения
export function check_csfr_for_post_request(targetunction) {
  // Будет возвращена измененная функция с дополнительным функционалом проверки и получения csfr
  return async function (...args) {
    //
    // Получение csfr токена из кук браузера
    let csfrFromCookies = getCSRFTokenFromCookie();
    //
    //Проверка наличия токена
    if (!csfrFromCookies) {
      console.log('Cookie dont have csfr token. Getting a new token:');
      //
      try {
        // Получение нового csfr токена. Его не надо куда-то присваивать, он автоматически сохранится в куках браузера
        await getCSRFTokenFromBack().then(response => {
          csfrFromCookies = getCSRFTokenFromCookie();
          //
          if (csfrFromCookies) {
            console.log(`Successful receipt of token: ${csfrFromCookies}`);
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
const getCSRFTokenFromBack = async () => {
  const response = await axios.get(
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
const getCSRFTokenFromCookie = () => {
  const cookieValue = document.cookie
                              .split('; ')
                              .find(row => row.startsWith('csrftoken='))
                              ?.split('=')[1];
  //
  return cookieValue ? cookieValue : '';
};