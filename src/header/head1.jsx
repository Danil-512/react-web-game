// import authorization from '../body/authorization';
// import './header.css'
// import { createBrowserRouter,  BrowserRouter as Router, Routes, Route, Link, useNavigate, useLocation } from "react-router-dom";
// import { postExit } from '../front_functions/functions.js'


// function head1() {
//   const location = useLocation()
//     return (
//       <div className='headerAll'>
        
//           <nav>
//             {
//               location.pathname == '/' && (
//                 <Link to="/reg" className='headerButtons'>Registration</Link>
//               )
//             }
//             {
//               location.pathname == '/auth' && (
//                 <Link to="/reg" className='headerButtons'>Registration</Link>
//               )
//             }
//             {
//               location.pathname == '/reg' && (
//                 <Link to="/auth" className='headerButtons'>Authorization</Link>
//               )
//             }
//             {
//               location.pathname == '/main' && (
//                 <Link to="/auth" className='headerButtons'>Authorization</Link>
//               )
//             }
//             {/* <Link to="/auth" className='headerButtons'>Authorization</Link>
//             <Link to="/main" className='headerButtons'>Main</Link> */}
//           </nav>

        
//       </div>
//     )
// }

// export default head1
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { postExit } from '../front_functions/functions.js';
import './header.css';

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
      </nav>
    </div>
  );
}

export default Head1;
