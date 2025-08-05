// NewArticle.jsx
import { useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

import '../body.css';


export const backServerPath = import.meta.env.VITE_MAIN_BACK_SERVER_PATH;

// Список статей по закону, передаваемому в параметре
function NewArticle() {
  const { lawId } = useParams();
  const [article_title, setarticleTitle] = useState(null);
  const [points, setPoints] = useState(['']); // Для добавления пунктов на странице
  const [responsibilities, setResponsibilities] = useState(
    {
      criminal: false,
      administrative: false,
      civil: false,
      other: false
    }
  );
  const [errorMessage, setErrorMessage] = useState(null); // Состояние для хранения ошибки
  //
  // Функция для очищения введенных данных
  const handleClearPointClick = async () => {
    // Очищение массива пунктов
    setPoints(['']);
    //
    // Сброс ответственностей на стандартные
    setResponsibilities({
      criminal: false,
      administrative: false,
      civil: false,
      other: false
    });
    //
    console.log('Очистка лишних пунктов произведена')
  }
  //
  // Добавление нового пункта
  const handleNewPointClick = () => {
    // Добавление нового пустого пункта
    setPoints([...points, '']);
    //
    // Добавление незаполненной ответственности
    setResponsibilities([...responsibilities, {
      criminal: false,
      administrative: false,
      civil: false,
      other: false
    }]);
  };
  //
  // Обновление конкретного пункта
  const handlePointChange = (index, value) => {
    console.log('handlePointChange')
    //
    // Получение списка с пунктами из хранимой переменной
    let newPoints = [...points];
    //
    // Обновление значения пункта по индексу
    newPoints[index] = value;
    //
    // Сохранение измененного списка пунктов
    setPoints(newPoints);
  };
  //
  // Обновление типа ответсвенности за нарушение статьи по переданному типу
  const handleResponsibilityChange = (responsibilityType) => {
    setResponsibilities(prev => ({
      ...prev,
      [responsibilityType]: !prev[responsibilityType]
    }));
  };
  //
  // Функция для получения CSRF-токена из кук
  const getCSRFToken = () => {
    // Получения csrf токена из кук
    const cookieValue = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)');
    //
    return cookieValue ? cookieValue.pop() : '';
  };
  //
  // Функция для отправления списка пунктов статьи на сервер
  const addPoints = async () => {
    // Обнуление текста ошибки
    setErrorMessage(null);
    //
    console.log('Current cookies:', document.cookie);
    //
    // Получение текущего csrf токена из кук
    const csrfToken = getCSRFToken();
    //
    console.log('CSRF Token:', csrfToken);
    //
    // Создание объекта для последующего отправления на бэк
    const postData = {
      article_title: article_title || '',
      points: points.filter(p => p.trim() !== '').map(p => ({ text: p })),
      responsibilities: responsibilities
    };
    //
    // Попытка отправления на бэк
    try {
      // Отправление запроса на бэк и получение ответа в переменную
      const response = await axios.post(
        `${backServerPath}/laws/${lawId}/newArticle/`,
        postData,
        {
          withCredentials: true,
          headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
          },
          xsrfCookieName: 'csrftoken',
          xsrfHeaderName: 'X-CSRFToken',
        }
      );
      //
      // Анализ ответа бэка
      if (response.data === 'NewArticleOK') {
        setErrorMessage('Статья успешно добавлена');
        //
        //// Сброс формы
        setPoints(['']);
        //
        setarticleTitle('');
        //
        setResponsibilities({
          criminal: false,
          administrative: false,
          civil: false,
          other: false
        });
      } else {
        setErrorMessage('Неизвестная ошибка при добавлении статьи');
      }
      //
      console.log('Response:', response.data);
    } catch (error) {
      // Вывод текста ошибки в консоль
      console.error('Error:', error);
      //
      // Анализ ошибки и вывод ошибки на страницу
      if (error.response) {
        if (error.response.status === 401) {
          setErrorMessage('Ошибка: Вы не авторизованы. Пожалуйста, войдите снова.');
        } else {
          setErrorMessage(`Ошибка сервера: ${error.response.status}`);
        }
      } else {
        setErrorMessage('Не удалось подключиться к серверу');
      }
    }
  };
  //
  // Изменение названия статьи
  const handleNametChange = (e) => {
    setarticleTitle(e)
  }
  //
  // Возвращаемая верстка
  return (
    <div className="new-article-div">
      <h2>Добавление новой статьи</h2>
    
      <p>ㅤ</p>

      {errorMessage && (
        <div style={{ 
          color: 'red', 
          padding: '10px', 
          margin: '10px 0', 
          border: '1px solid red',
          borderRadius: '4px'
        }}>
          {errorMessage}
          {errorMessage.includes('аутентификации') && (
            <div>
              <a href="/auth" style={{ color: 'blue' }}>Перейти на страницу входа</a>
            </div>
          )}
        </div>
      )}

      <span>
        Название статьи
      </span>

      <input 
        type="text"
        value={article_title}
        onChange={(e) => handleNametChange(e.target.value)}  
      />

      {points.map((point, index) => (
        <div key={index}>
          <span>
            Пункт статьи
          </span>
          <input 
            type="text"
            value={point}
            onChange={(e) => handlePointChange(index, e.target.value)}  
          />
        </div>
      ))}

      <div>
        <span>Уголовная: </span>
        <input 
          type="checkbox" 
          checked={responsibilities?.criminal || false}
          onChange={() => handleResponsibilityChange('criminal')}
        />

        <span> Административная: </span>
        <input 
          type="checkbox" 
          checked={responsibilities?.administrative || false}
          onChange={() => handleResponsibilityChange('administrative')}
        />

        <span> Гражданская: </span>
        <input 
          type="checkbox" 
          checked={responsibilities?.civil || false}
          onChange={() => handleResponsibilityChange('civil')}
        />

        <span> Иная: </span>
        <input 
          type="checkbox" 
          checked={responsibilities?.other || false}
          onChange={() => handleResponsibilityChange('other')}
        />
      </div>

      <div id="parent"></div>

      <p>ㅤ</p>

      <button onClick={handleNewPointClick}>Новый пункт статьи</button>

      <button onClick={handleClearPointClick}>Очистить</button>

      <p>ㅤ</p>
      
      <button onClick={addPoints}>
        Добавить статьи
      </button>
    </div>
  );
}

export default NewArticle;