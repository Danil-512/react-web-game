// import React, { useState, useEffect, useRef } from 'react';
// import './body.css'

// // Адрес бэкенд сервера: 
// const backServerPath = 'http://127.0.0.1:8000/';

// // ----------------------------------------------------------------------------------------------------------------------------------------------/
// // /Возвращаемая функция
// function mainWindow() {


//     // /-------------------------------------------------------------------------------------------------------
//     // /Возвращаемая верстка
//     return (
//         <div class="authorization" id='div1' key='div1'>
//             <p className="auth1">Главная страница</p>
//         </div>
//     )
//     // Возвращаемая верстка/
//     // -------------------------------------------------------------------------------------------------------/

// }
// // Возвращаемая функция/
// // ----------------------------------------------------------------------------------------------------------------------------------------------/


// // export default mainWindow;
// import React, { useState, useEffect } from 'react';
// import { Link } from 'react-router-dom';
// import axios from 'axios';
// import './body.css';

// const backServerPath = 'http://127.0.0.1:8000/';

// function MainWindow() {
//   const [laws, setLaws] = useState([]);

//   useEffect(() => {
//     const fetchLaws = async () => {
//       try {
//         const response = await axios.get(`${backServerPath}laws`);
//         setLaws(response.data);
//       } catch (error) {
//         console.error('Ошибка при загрузке законов:', error);
//       }
//     };
//     fetchLaws();
//   }, []);

//   return (
//     <div className="authorization">
//       <h1 className="auth1">Главная страница</h1>
//       <div className="laws-list">
//         {laws.map((law) => (
//           <div key={law.id} className="law-item">
//             <h3>{law.title}</h3>
//             <p className="law-excerpt">{law.excerpt}</p>
//             <Link 
//               to={`/laws/${law.id}`} 
//               className="details-button"
//               state={{ lawData: law }} // Передача данных через state
//             >
//               Подробнее
//             </Link>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }

// export default MainWindow;


import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './body.css';
const backServerPath = 'http://127.0.0.1:8000/';

function MainWindow() {
    const [laws, setLaws] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    useEffect(() => {
        const fetchLaws = async () => {
        try {
            const response = await axios.get('/api/laws');
            
            console.log(response.data)

            const response1 = await axios.get(`/api/laws/${1}/`);
            
            const articlesResponse = await axios.get(`/api/laws/${lawId.toString()}`);
            

            console.log(response1.data)

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

    return (
        <div className="main-window">
        <h1>Актуальное законодательство</h1>
        <div className="laws-grid">
            {laws.map((law) => (
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
        </div>
        </div>
  );
}

export default MainWindow;