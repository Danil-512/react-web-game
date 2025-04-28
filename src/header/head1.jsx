import { Link, useLocation, useNavigate } from 'react-router-dom';
import { postExit } from '../front_functions/functions.js';
import './header.css';
import { getVariables } from '../sessionlVariables.js'


function Head1() {
  const location = useLocation();
  const navigate = useNavigate();

  const handleAuthClick = async () => {
    if (location.pathname === '/main') {
      try {
        await postExit();
      } catch (error) {
        console.error('Ошибка выхода:', error);
      }
    }
    navigate('/auth');
  };

  const handleMainClick = async () => {
    navigate('/main');
  };

  const handleLawsClick = async () => {
    navigate('/laws');
  };

  const handleArticlesClick = async () => {
    console.log(location.pathname);
    let path = location.pathname
    path = path.split('/').reverse()
    console.log(`path is: ${path}`)
    navigate(`/laws/${path[1]}`);
  };
  

  
  const isArcticlesPage = /^\/laws\/\d+$/.test(location.pathname)
  const isArticleTextLawPage = /^\/laws\/\d+\/\d+$/.test(location.pathname)

  
  return (
    <div className='headerAll'>
      <nav>
        {location.pathname === '/' && (
          <Link to="/reg" className='headerButtons'>Регистрация</Link>
        )}
        {location.pathname === '/auth' && (
          <Link to="/reg" className='headerButtons'>Регистрация</Link>
        )}
        {location.pathname === '/reg' && (
          <Link to="/auth" className='headerButtons'>Вход</Link>
        )}
        {location.pathname === '/main' && (
          <button onClick={handleAuthClick} className='headerButtons'>
            Сменить пользователя
          </button>
        )}
        {location.pathname === '/laws'
          && 
          (
          <button onClick={handleMainClick} className='headerButtons'>
            Главное меню
          </button>
          )
        }
        {isArcticlesPage
          && 
          (
          <button onClick={handleLawsClick} className='headerButtons'>
            Законы
          </button>
          )
        }
        {isArticleTextLawPage
          && 
          (
          <button onClick={handleArticlesClick} className='headerButtons'>
            Статьи закона
          </button>
          )
        }
      </nav>
      {
        getVariables()[1] != null &&
        <div className='headerUserInfo'>
          <p>
            Пользователь: 
            <span>
              {getVariables()[1]}
            </span>
          </p>
          <p>
            Права:
            <span>
              {getVariables()[2]}
            </span>
          </p>
        </div>
      }
      
    </div>
  );
}

export default Head1;
