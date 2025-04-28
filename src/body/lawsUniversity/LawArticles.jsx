// LawArticles.jsx (новый компонент)
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import '../body.css';
import { useNavigate } from 'react-router-dom';

// Список статей по закону, передаваемому в параметре
function LawArticles() {
  const { lawId } = useParams();
  const [lawsList, setLawsList] = useState([]); // Список получаемых законов
  const [articles, setArticles] = useState([]); // Список получаемых статей
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
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

  return (
    <div className="law_all_body">
      <h2>Статьи закона</h2>
      {articles.map((article) => (
        <div key={article.id} className="law-articles">
          <div>
            <p>-----------------</p>
            <p>Id: {article.article_number}</p>
            <p>No: {article.article_title}</p>
            <p>{article.article_descr}</p>
            <Link 
              to={`/laws/${lawId}/${article.article_number}`} 
              className="link-article"
              //state={[lawId, article.article_number]}
            >
              Полный текст статьи
            </Link>
          </div>
        </div>
      ))}
      <button className='add-article-to-law' onClick={handleNewArticleClick}>
        Добавить статью
      </button>
    </div>
  );
}

export default LawArticles;