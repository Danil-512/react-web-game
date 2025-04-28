import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import '../body.css';
import { useNavigate } from 'react-router-dom';

function MainWindow() {
    const [laws, setLaws] = useState([]);
    const [law_id, setLawId] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    // Объект для перехода на другую страницу
    const navigate = useNavigate();

    useEffect(() => {
        const fetchLaws = async () => {
        try {
            const response = await axios.get('/api/laws');
            
            console.log(response.data)

            //const response1 = await axios.get(`/api/laws/${1}/`);
            
            //const articlesResponse = await axios.get(`/api/laws/${lawId.toString()}`);
            

            //console.log(response1.data)

            setLaws(response.data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
        };
        fetchLaws();
    }, []);

    if (loading) return <div className="loading">Загрузка законов...</div>;
    if (error) return <div className="error">Ошибка: {error}</div>;

    async function handleButtonArticlesClick() {
      console.log(`-----------------------------------------`)
      console.log(`Событие на странице: handleButtonArticlesClick - Laws`)
      console.log(`path is: /laws/${law_id}`);
      navigate(`/laws/${law_id}`);
    }

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