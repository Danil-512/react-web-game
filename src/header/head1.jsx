import './header.css'
import { createBrowserRouter,  BrowserRouter as Router, Routes, Route, Link, useNavigate, useLocation } from "react-router-dom";


function head1() {
  const location = useLocation()
    return (
      <div className='headerAll'>
        
          <nav>
            {
              location.pathname == '/auth' && (
                <Link to="/reg" className='headerButtons'>Registration</Link>
              )
            }
            {
              location.pathname == '/reg' && (
                <Link to="/auth" className='headerButtons'>Authorization</Link>
              )
            }
            {
              location.pathname == '/main' && (
                <Link to="/auth" className='headerButtons'>Authorization</Link>
              )
            }
            {/* <Link to="/auth" className='headerButtons'>Authorization</Link>
            <Link to="/main" className='headerButtons'>Main</Link> */}
          </nav>

        
      </div>
    )
}

export default head1
