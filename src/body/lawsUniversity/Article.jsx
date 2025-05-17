// LawArticles.jsx (новый компонент)
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import '../body.css';
import { useNavigate } from 'react-router-dom';
import './law.css'

// Список статей по закону, передаваемому в параметре
function ArticlesText() {
  console.log('%cFunction ArticlesText starting.', 'color: red')

  const { lawId, articleId } = useParams();
  const [text, setText] = useState(true);
  const [splitData, setSplitData] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Получение списка статей закона
        console.log("\nОтправдение get запроса с законами 1")

        const textResponse = await axios.get(`http://127.0.0.1:8000/laws/${lawId}/${articleId}`);

        console.log(`articlesResponse.data is: ${textResponse.data}`);
        const data = textResponse.data 
        setText(data);
        setSplitData(data.split('^;'));
        console.log(splitData)
      } catch (err) {
        console.error('Полная ошибка:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [lawId, articleId]);

  if (loading) return <div className="loading">Загрузка текста статьи...</div>;
  if (error) return <div className="error">Ошибка: {error}</div>;

  return (
    <div key={articleId} className="law_all_body">        
        <h3>Текст статьи: </h3>
        <p>...</p>
        {splitData.map((data) => (
            <div className="articles-list">
                {data.split('\n').map((data1) => (
                  <p>{data1}</p>
                ))}
            </div>
        ))}
    </div>
  );
}

export default ArticlesText;