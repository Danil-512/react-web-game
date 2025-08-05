// Laws.jsx
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

import '../body.css';


export const lawsServerPath = import.meta.env.VITE_LAWS_BACK_SERVER_PATH;

function MainWindow() {
  const [laws, setLaws] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  //
  useEffect(() => {
    const fetchLaws = async () => {
      try {
        const response = await axios.get(`${lawsServerPath}/rest_api/laws`);
        //
        console.log(response.data)
        //
        setLaws(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    //
    fetchLaws();
  }, [] );
  //
  //// Отображение текущего статуса на странице
  if (loading) return <div className="loading">Загрузка законов...</div>;
  //
  if (error) return <div className="error">Ошибка: {error}</div>;
  //
  // Возаращаемая верстка
  return (
    <div className="law_all_body">
      <h1>Актуальное законодательство</h1>

      <div className="laws-grid">
        {laws.map((law) => (
          <div key={law.id} className="law-articles">
            <p>--------------------------</p>

            <p>Номер закона: {law.law_id}</p>
                
            <div className="law-header">
              <h2>{law.law_title}</h2>
                
              <div className="law-meta">
                <p>№ {law.law_number}</p>

                <p>{new Date(law.law_date).toLocaleDateString()}</p>
              </div>
            </div>

            <Link 
              to={`/laws/${law.law_id}`} 
              className="link-law-articles"
              state={{ law }}
            >
               Изучить статьи закона
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MainWindow;