// LawArticles.jsx (новый компонент)
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import '../body.css';
import { useNavigate } from 'react-router-dom';

// Список статей по закону, передаваемому в параметре
function NewArticle() {
  const { lawId } = useParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const [articleTitle, setarticleTitle] = useState(null);
  const [points, setPoints] = useState(['']); // Для добавления пунктов на странице
  const [responsibilities, setResponsibilities] = useState(
    {
      criminal: false,
      administrative: false,
      civil: false,
      other: false
    }
  );


  const handleClearPointClick = async () => {
    //parent = document.querySelector('#parent');
    setPoints(['']);
    setResponsibilities({
      criminal: false,
      administrative: false,
      civil: false,
      other: false
    });
    console.log('Очистка лишних пунктов.')
  }


  // Добавление нового пункта
  const handleNewPointClick = () => {
    setPoints([...points, '']); // Добавляем новый пустой пункт
    setResponsibilities([...responsibilities, {
    criminal: false,
    administrative: false,
    civil: false,
    other: false
  }]);
  };

  // Обновление конкретного пункта
  const handlePointChange = (index, value) => {
    console.log('handlePointChange')
    let newPoints = [...points];
    newPoints[index] = value;
    setPoints(newPoints);
  };




  const handleResponsibilityChange = (responsibilityType) => {
    setResponsibilities(prev => ({
      ...prev,
      [responsibilityType]: !prev[responsibilityType]
    }));
  };

  
 
  // Функция для отправления списка пунктов статьи на сервер
  const addPonts = async () => {
    // Формируем массив объектов с пунктами и их ответственностями
    const postData = points.map((point, index) => ({
      text: point,
    }));

    // Фильтруем пустые пункты
    const filteredData = postData.filter(item => item.text.trim() !== '');

    console.log('Отправления нового списка статей на сервер.');

    // /-------------------------------------------------------------------------------------------------------
    // /axios post
    console.log("Новый пункт. Начало отправки")
    let status1 = "NewArticleNOTOK"
    console.log(`Отправляемые данные: ${{ points: filteredData }}`)

    const response = await axios.post(`http://127.0.0.1:8000/laws/${lawId}/newArticle/`
                                    ,{ 
                                      articleTitle: articleTitle,
                                      points: filteredData,
                                      responsibilities: responsibilities
                                    }); 

    console.log(`Response is: ${response.data}`);

    if (response.data == 'NewArticleOK') {
      console.log('Статья добавлена');
      setPoints(['']);
      setarticleTitle('');
      setResponsibilities({
        criminal: false,
        administrative: false,
        civil: false,
        other: false
      });
    }
    // axios post/
    // -------------------------------------------------------------------------------------------------------/
  }

  const handleNametChange = (e) => {
    setarticleTitle(e)
    console.log('Название статьи:', articleTitle)
  }

  return (
    <div className="new-article-div">
      <h2>Добавление новой статьи</h2>
      <span>
        Название статьи
      </span>
      <input 
        type="text"
        value={articleTitle}
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
      <button onClick={handleNewPointClick}>Новый пункт статьи</button>
      <button onClick={handleClearPointClick}>Очистить</button>


      {/* Демонстрация введеных значений */}
      <div>
        <h3>Текущие пункты:</h3>
        <ul>
          {points.map((point, index) => (
            <li key={index}>
              {point || `<пустой пункт ${index + 1}>`}
            </li>
          ))}
        </ul>
        <p>Ответственности:</p>
        <div>
                Ответственность: 
                {responsibilities?.criminal && "Уголовная "}
                {responsibilities?.administrative && "Административная "}
                {responsibilities?.civil && "Гражданская "}
                {responsibilities?.other && "Иная"}
                {!responsibilities?.criminal && 
                !responsibilities?.administrative && 
                !responsibilities?.civil && 
                !responsibilities?.other && "Не указана"}
              </div>
      </div>
      
      <button onClick={addPonts}>
        Добавить статьи
      </button>
    </div>
  );
}

export default NewArticle;