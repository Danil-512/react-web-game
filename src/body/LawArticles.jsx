// LawArticles.jsx (новый компонент)
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import './body.css';

function LawArticles() {
  const { lawId } = useParams();
  const [lawsList, setLawsList] = useState([]); // Список получаемых законов
  const [articles, setArticles] = useState([]); // Список получаемых статей
  const [articles2, setArticles2] = useState([]); // Список получаемых статей
  const [lawInfo, setLawInfo] = useState([]); // Статья целиком - тоже список из 1 элемента
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Получаем основную информацию о законе
        console.log("Отправдение get запроса с законами 1")
        const path1 = `/api/laws/1/articles`

        const rewrite =  path1.replace('/api', '');

        console.log(rewrite);


        
        const lawResponse = await axios.get(`/api/laws/1/articles`);

        const lawsResponse = await axios.get(`/api/laws`);
        //const lawResponse = await axios.get(`/api/laws/${lawId.toString()}/articles`);
        const articlesResponse = await axios.get(`/api/laws/1`);

        //const articlesResponse = await axios.get(`/api/laws/${lawId.toString()}`);


        console.log(`/api/laws/${lawId}`);
        /*
        // Проверка типа данных
        if (!Array.isArray(lawResponse.data)) {
          console.log('Ожидался массив статей');
          throw new Error('Ожидался массив статей');
       }
        */
      //  // Проверяем статусы ответов
      //  if (lawsResponse.status !== 200 || 
      //   lawResponse.status !== 200) {
      // throw new Error('Ошибка получения данных');
      // }

      

      /*
      // Проверяем формат данных
      if (!Array.isArray(articlesResponse.data)) {
        throw new Error('Некорректный формат статей');
      
      }
        */
        console.log("Отправдение get запроса с статьями 2")
        //console.log(lawsResponse.data);
        console.log(`lawResponse.data is: ${lawResponse.data}`);
        console.log(`articlesResponse.data is: ${articlesResponse.data}`);
        console.log(`lawsResponse.data is: ${lawsResponse.data}`);

        //print(articlesResponse);
        // Обновляем состояние
        // setLawsList(lawsResponse.data);
        setLawInfo(lawResponse.data);
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

  return (
    <div className="law-articles">
      <div className="header-section">
        <Link to="/main" className="back-button">
          &larr; Назад к списку законов
        </Link>
        <div className="laws-preview">
          {lawsList.slice(0, 3).map(law => (
            <div key={law.id} className="law-preview-card">
              <h4>{law.title}</h4>
              <span>№ {law.number}</span>
            </div>
          ))}
        </div>
      </div>
      
      
      {/* {lawInfo && (
        <div className="law-info">
          <h1>{lawInfo.title}</h1>
          <div className="law-meta">
            <span>Номер закона: {lawInfo.number}</span>
            <span>Дата принятия: {new Date(lawInfo.date).toLocaleDateString()}</span>
          </div>
        </div>
      )} */}

      {lawInfo.map((law) => (
        <div key={law.id} className="law-card">
          <div className="law-header">
            <h2>{law.title}</h2>
            <div className="law-meta">
              <span>№ {law.number}</span>
                <span>{new Date(law.date).toLocaleDateString()}</span>
              </div>
            </div>
            <Link 
              to={`/laws/${law.id}`} 
              className="view-articles-button"
              state={{ law }}
            >
              Изучить статьи →
            </Link>
          </div>
        
      
      ))}
      {/* Добавляем блок со статьями */}
      {/* <div className="articles-list">
        <h2>Статьи закона:</h2>
        {articles.length > 0 ? (
          <ul>
            {articles.map(article => (
              <li key={article.id}>
                <Link 
                  to={`/laws/${lawId}/${article.id}`}
                  className="article-link"
                >
                  {article.title}
                </Link>
              </li>
            ))}
          </ul>
        ) : (
          <p>Нет доступных статей для этого закона</p>
        )}
      </div> */}
      {/* <div className="articles-list">
        <h2>Статьи закона:</h2>
        {articles.length > 0 ? (
          <ul>
            {articles.map(article => (
              <li key={article.id}>
                <Link 
                  to={`/laws/${lawId}/${article.id}`}
                  className="article-link"
                >
                  {article.title}
                </Link>
              </li>
            ))}
          </ul>
        ) : (
          <p>Нет доступных статей для этого закона</p>
        )}
      </div> */}
    </div>
  );
}

export default LawArticles;