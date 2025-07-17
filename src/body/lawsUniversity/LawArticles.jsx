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
  const [articlesCount, setArticlesCount] = useState(0); // Количество получаемых статей
  const [articlesCount1, setArticlesCount1] = useState(0); // Количество получаемых статей
  const [articlesCount2, setArticlesCount2] = useState(0); // Количество получаемых статей
  const [articlesCount3, setArticlesCount3] = useState(0); // Количество получаемых статей
  const [articlesCount4, setArticlesCount4] = useState(0); // Количество получаемых статей
  const [activeFilter, setActiveFilter] = useState('all'); // Текущий активный фильтр
  const [filteredArticles, setFilteredArticles] = useState([]); // Отфильтрованные статьи
  const [allArticles, setAllArticles] = useState([]); 

  const [counters, setCounters] = useState({
    total: 0,
    criminal: 0,      // Уголовная
    administrative: 0, // Административная
    civil: 0,         // Гражданская
    other: 0          // Иная
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  
  const handleNewArticleClick = async () => {
    navigate(`/laws/${lawId}/newArticle`);
  }

  // Кнопки с фильтрацией типов ответсвенности
  const handleCriminalClick = async () => {
    console.log('Нажата кнопка фильтрации: только уголовная ответсвенность');
    setActiveFilter('criminal');
    filterArticles('Уголовная');
  }
  const handleAdministrativeClick = async () => {
    console.log('Нажата кнопка фильтрации: только административная ответсвенность');
    setActiveFilter('administrative');
    filterArticles('Административная');
  }
  const handleCivilClick = async () => {
    console.log('Нажата кнопка фильтрации: только гражданская ответсвенность');
    setActiveFilter('civil');
    filterArticles('Гражданская');
  }
  const handleOtherClick = async () => {
    console.log('Нажата кнопка фильтрации: только иная ответсвенность');
    setActiveFilter('other');
    filterArticles('other');
  }
  const handleResetFilter = () => {
    setActiveFilter('all');
    setFilteredArticles(allArticles);
  }

  const filterArticles = (filterType) => {
    if (filterType === 'other') {
      const filtered = allArticles.filter(article => {
        const responsibility = article.article_responsobility || '';
        return responsibility.trim() && 
               !responsibility.includes('Уголовная') && 
               !responsibility.includes('Административная') && 
               !responsibility.includes('Гражданская');
      });
      setFilteredArticles(filtered);
    } else {
      const filtered = allArticles.filter(article => 
        (article.article_responsobility || '').includes(filterType)
      );
      setFilteredArticles(filtered);
    }
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        let criminalCount = 0;
        let administrativeCount = 0;
        let civilCount = 0;
        let otherCount = 0;

        // Получение списка статей закона
        console.log("\nОтправдение get запроса с законами 1")

        const articlesResponse = await axios.get(`http://127.0.0.1:7000/rest_api/laws/${lawId}`);

        console.log(`/api/laws/${lawId}`);
  
        console.log(`articlesResponse.data is: ${articlesResponse.data}`);

        setArticles(articlesResponse.data);
        setArticlesCount(articlesResponse.data.length);

        setAllArticles(articlesResponse.data);
        setFilteredArticles(articlesResponse.data);


        articlesResponse.data.forEach(article => {
          const responsibility = article.article_responsobility || '';
          
          if (responsibility.includes('Уголовная')) criminalCount++;
          if (responsibility.includes('Административная')) administrativeCount++;
          if (responsibility.includes('Гражданская')) civilCount++;
          
          // Если ответственность есть, но не подпадает под основные типы
          if (responsibility.trim() && 
              !responsibility.includes('Уголовная') && 
              !responsibility.includes('Административная') && 
              !responsibility.includes('Гражданская')) {
            otherCount++;
          }
        });

        setCounters({
          total: articlesResponse.data.length,
          criminal: criminalCount,
          administrative: administrativeCount,
          civil: civilCount,
          other: otherCount
        });
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

  // articles.map((article) => (
  //   setArticlesCount(articles + 1)
  // ));

  // return (
  //   <div className="law_all_body">
  //     <p>
  //       <span>Отобразить статьи только с типом ответсвенности:</span>
  //       <p>
  //         <button onClick={handleCriminalClick}>Уголовной</button>
  //         <button onClick={handleAdministrativeClick}>Административная</button>
  //         <button onClick={handleCivilClick}>Гражданская</button>
  //         <button onClick={handleOtherClick}>Иная</button>
  //       </p>
  //     </p>
  //     <h2>Статьи закона</h2>
  //     {articles.map((article) => (
  //       <div key={article.id} className="law-articles">
  //         <div>
  //           <p>-----------------</p>
  //           <p>Id: {article.article_number}</p>
  //           <p>No: {article.article_title}</p>
  //           <p>{article.article_descr}</p>
  //           <Link 
  //             to={`/laws/${lawId}/${article.article_number}`} 
  //             className="link-article"
  //             //state={[lawId, article.article_number]}
  //           >
  //             Полный текст статьи
  //           </Link>
  //           <p>Типы ответственности:{article.article_responsobility}</p>
  //         </div>
  //       </div>
  //     ))}
  //     <p>Всего статей в законе: {counters.total}</p>
  //     <p>Статей с уголовной ответственностью: {counters.criminal}</p>
  //     <p>Статей с административной ответственностью: {counters.administrative}</p>
  //     <p>Статей с гражданская ответственностью: {counters.civil}</p>
  //     <p>Статей с иной ответственностью: {counters.other}</p>
     
  //     <button className='add-article-to-law' onClick={handleNewArticleClick}>
  //       Добавить статью
  //     </button>
  //   </div>
  // );
  return (
    <div className="law_all_body">
      <div className="filter-section">
        <span>Отобразить статьи только с типом ответственности: </span>
        <div className="filter-buttons">
          <button 
            onClick={handleResetFilter}
            className={activeFilter === 'all' ? 'active' : ''}
          >
            Все
          </button>
          <button 
            onClick={handleCriminalClick}
            className={activeFilter === 'criminal' ? 'active' : ''}
          >
            Уголовная ({counters.criminal})
          </button>
          <button 
            onClick={handleAdministrativeClick}
            className={activeFilter === 'administrative' ? 'active' : ''}
          >
            Административная ({counters.administrative})
          </button>
          <button 
            onClick={handleCivilClick}
            className={activeFilter === 'civil' ? 'active' : ''}
          >
            Гражданская ({counters.civil})
          </button>
          <button 
            onClick={handleOtherClick}
            className={activeFilter === 'other' ? 'active' : ''}
          >
            Иная ({counters.other})
          </button>
        </div>
      </div>

      <h2>Статьи закона {activeFilter !== 'all' ? `(${activeFilter})` : ''}</h2>
      <p>--</p>
      {filteredArticles.length === 0 ? (
        <div className="no-articles">
          {activeFilter === 'all' 
            ? 'В этом законе пока нет статей' 
            : 'Нет статей с выбранным типом ответственности'}
        </div>
      ) : (
        filteredArticles.map((article) => (
          <div key={article.article_id} className="law-article">
            <div className="article-header">
              <h3>Статья {article.article_number}</h3>
              <p className="article-title">{article.article_title}</p>
            </div>
            <div className="article-content">
              <p className="article-description">
                {article.article_descr || 'Нет описания'}
              </p>
              <Link 
                to={`/laws/${lawId}/${article.article_number}`} 
                className="link-article"
              >
                Полный текст статьи
              </Link>
              <p className="article-responsibility">
                <strong>Типы ответственности:</strong> {article.article_responsobility || 'Не указаны'}
              </p>
            </div>
            <p>---</p>
          </div>
        ))
      )}
      <div className="counters-section">
        <p>Всего статей в законе: {counters.total}</p>
        <p>Статей с уголовной ответственностью: {counters.criminal}</p>
        <p>Статей с административной ответственностью: {counters.administrative}</p>
        <p>Статей с гражданской ответственностью: {counters.civil}</p>
        <p>Статей с иной ответственностью: {counters.other}</p>
      </div>
      
      <button className='add-article-to-law' onClick={handleNewArticleClick}>
        Добавить статью
      </button>
    </div>
  );
}

export default LawArticles;