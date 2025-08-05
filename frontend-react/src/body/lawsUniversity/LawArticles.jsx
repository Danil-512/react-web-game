// LawArticles.jsx
import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

import '../body.css';


export const lawsServerPath = import.meta.env.VITE_LAWS_BACK_SERVER_PATH;

// Список статей по закону, передаваемому в параметре
function LawArticles() {
  const { lawId } = useParams();
  const [activeFilter, setActiveFilter] = useState('all'); // Текущий активный фильтр
  const [filteredArticles, setFilteredArticles] = useState([]); // Отфильтрованные статьи
  const [allArticles, setAllArticles] = useState([]); 
  //
  const [counters, setCounters] = useState({
    total: 0,
    criminal: 0,       // Уголовная
    administrative: 0, // Административная
    civil: 0,          // Гражданская
    other: 0           // Иная
  });
  //
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  //
  // Переход на страницу добавления статей
  const handleNewArticleClick = async () => {
    navigate(`/laws/${lawId}/newArticle`);
  }
  //
  //// Кнопки с фильтрацией типов ответсвенности
  // Фильтрация отображаемых статей на странице - только уголовные
  const handleCriminalClick = async () => {
    console.log('Нажата кнопка фильтрации: только уголовная ответсвенность');
    //
    setActiveFilter('criminal');
    //
    filterArticles('Уголовная');
  }
  //
  // Фильтрация отображаемых статей на странице - только административные
  const handleAdministrativeClick = async () => {
    console.log('Нажата кнопка фильтрации: только административная ответсвенность');
    setActiveFilter('administrative');
    filterArticles('Административная');
  }
  //
  // Фильтрация отображаемых статей на странице - только гражданские
  const handleCivilClick = async () => {
    console.log('Нажата кнопка фильтрации: только гражданская ответсвенность');
    setActiveFilter('civil');
    filterArticles('Гражданская');
  }
  //
  // Фильтрация отображаемых статей на странице - только иные
  const handleOtherClick = async () => {
    console.log('Нажата кнопка фильтрации: только иная ответсвенность');
    //
    // Изменение активного фильтра
    setActiveFilter('other');
    //
    filterArticles('other');
  }
  //
  // Фильтрация отображаемых статей на странице - все
  const handleResetFilter = () => {
    setActiveFilter('all');
    // 
    // Установить список отфильтрованных статей - они отображаются на странице
    setFilteredArticles(allArticles);
  }
  //
  // Функция для фильтрации 
  const filterArticles = (filterType) => {
    if (filterType === 'other') {
      const filtered = allArticles.filter(article => {
        const responsibility = article.article_responsobility || '';
        //
        return responsibility.trim() && 
               !responsibility.includes('Уголовная') && 
               !responsibility.includes('Административная') && 
               !responsibility.includes('Гражданская');
      });
      //
      setFilteredArticles(filtered);
    } else {
      const filtered = allArticles.filter(article => 
        (article.article_responsobility || '').includes(filterType)
      );
      //
      // Установить список отфильтрованных статей - они отображаются на странице
      setFilteredArticles(filtered);
    }
  }
  //
  useEffect(() => {
    const fetchData = async () => {
      try {
        let criminalCount = 0;
        let administrativeCount = 0;
        let civilCount = 0;
        let otherCount = 0;
        //
        // Отправление запроса на получение списка статей закона и присвоение ответа переменной
        const articlesResponse = await axios.get(`${lawsServerPath}/rest_api/laws/${lawId}`);
        //
        console.log(`articlesResponse.data is: ${articlesResponse.data}`);
        //
        // Заполнение массива со статьями из ответа бэка
        setAllArticles(articlesResponse.data);
        //
        // Заполнение массива с отфильтрованными статьями из ответа бэка
        setFilteredArticles(articlesResponse.data);
        //
        // Цикл по статьям закона - определение типа ответсвенности для изменения счетчиков ответсвенностей
        articlesResponse.data.forEach(article => {
          const responsibility = article.article_responsobility || '';
          //
          // Если относится к какому-либо типу, увеличиваем соответствующий счетчик
          if (responsibility.includes('Уголовная')) criminalCount++;
          if (responsibility.includes('Административная')) administrativeCount++;
          if (responsibility.includes('Гражданская')) civilCount++;
          //
          // Если ответственность есть, но не подпадает под основные типы
          if (responsibility.trim() && 
              !responsibility.includes('Уголовная') && 
              !responsibility.includes('Административная') && 
              !responsibility.includes('Гражданская')) {
            otherCount++;
          }
        });
        //
        // Присвоение полученных количеств типов статей внешней переменной
        setCounters({
          total: articlesResponse.data.length,
          criminal: criminalCount,
          administrative: administrativeCount,
          civil: civilCount,
          other: otherCount
        });
      } catch (err) {
        console.error('Полная ошибка:', err);
        //
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    //
    fetchData();
  }, [lawId]);
  //
  //// Отображение текущего статуса на странице
  if (loading) return <div className="loading">Загрузка статей...</div>;
  //
  if (error) return <div className="error">Ошибка: {error}</div>;     
  //
  // Возвращаемая верстка
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