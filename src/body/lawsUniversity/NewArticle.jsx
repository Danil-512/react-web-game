// LawArticles.jsx (новый компонент)
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import '../body.css';
import { useNavigate } from 'react-router-dom';

// Список статей по закону, передаваемому в параметре
function NewArticle() {
  const { lawId } = useParams();
  const [lawsList, setLawsList] = useState([]); // Список получаемых законов
  const [articles, setArticles] = useState([]); // Список получаемых статей
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pointCount, setPointCount] = useState(1);
  const navigate = useNavigate();
  
  const handleNewArticleClick = async () => {
    navigate(`/laws/${lawId}/newArticle`);
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Получение списка статей закона
        console.log("\nОтправдение get запроса с законами 1")

        const articlesResponse = await axios.get(`http://127.0.0.1:8000/laws/${lawId}`);

        console.log(`/api/laws/${lawId}`);
  
        console.log(`articlesResponse.data is: ${articlesResponse.data}`);

        setArticles(articlesResponse.data);
      } catch (err) {
        console.error('Полная ошибка:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [lawId]);

  if (loading) return <div className="loading">Загрузка статей...</div>;
  if (error) return <div className="error">Ошибка: {error}</div>;

  const handleNewPointClick = async () => {
    parent = document.querySelector('#parent');

    let span = document.createElement('span')
    let input = document.createElement('input')
    let button = document.createElement('button')
    span.textContent = 'Пункт статьи:';
    
    
    parent.appendChild(span)
    parent.appendChild(input)
    // for (let i = 1; i <= pointCount; i++) {
    //   let p = document.createElement('p');
    //   parent.appendChild(p);
    // }
    
  }

 
  return (
    <div className="new-article-div">
      <h2>Добавление новой статьи</h2>
      <div>
        <span>Пункт статьи:</span>
        <input type="text" />
      </div>
      <div id="parent"></div>
      <button onClick={handleNewPointClick}>Новый пункт статьи</button>
    </div>
  );
}

export default NewArticle;