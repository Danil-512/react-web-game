import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import './body.css';

function ArticleDetails() {
  const { lawId, articleId } = useParams(); // Получаем оба параметра
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`/api/laws/${lawId}/${articleId}`);
        setArticle(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [lawId, articleId]);

  if (loading) return <div className="loading">Загрузка статьи...</div>;
  if (error) return <div className="error">Ошибка: {error}</div>;

  return (
    <div className="article-details">
      <Link to={`/laws/${lawId}`} className="back-button">
        &larr; Назад к статьям
      </Link>
      
      {article && (
        <>
          <h1>{article.title}</h1>
          <div className="meta-info">
            <span>Статья №{article.id}</span>
            <span>Дата: {new Date(article.date).toLocaleDateString()}</span>
          </div>
          <div className="content">
            {article.text}
          </div>
        </>
      )}
    </div>
  );
}

export default ArticleDetails;