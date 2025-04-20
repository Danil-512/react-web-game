// import React, { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'
// import { createRoot } from 'react-dom/client'
// import Head1 from './header/head1.jsx'
// import Body1 from './body/body1.jsx'
// import Authorization from './body/authorization.jsx'
// import Register from './body/register.jsx'
// import MainWindow from './body/mainWindow.jsx';

// import { BrowserRouter, Routes, Route, Outlet } from 'react-router-dom';

// // const App = () => {
// //   return (
// //     <BrowserRouter>
// //       <Routes>
// //         <Route path='/' element={<Layout />}>
// //         </Route>
// //       </Routes>
// //     </BrowserRouter>
// //   );
// // };

// // const Layout = () => {
// //   return (
// //     <div>
// //       <header className="head1"> 
// //         <Head1 />
// //       </header>
// //       <div className="body1">
// //         <Body1 />
// //       </div>
// //     </div>
// //   );
// // };



// function App() {
//   return (
//     <BrowserRouter>
//       <div>
//         <header className="head1"> 
//           <Head1 />
//         </header>
//         <div className="body1">
//           <Routes>
//             <Route path="/" element={<Body1 />}>
//               <Route index element={<Authorization />} />
//               <Route path='auth' element={<Authorization />} />
//               <Route path='reg' element={<Register />} />
//               <Route path='main' element={<MainWindow />} />
//             </Route>
//           </Routes>
//         </div>
//       </div>
//     </BrowserRouter>
//   )
// }


// export default App




import React, { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { createRoot } from 'react-dom/client'
import Head1 from './header/head1.jsx'
import Body1 from './body/body1.jsx'
import Authorization from './body/authorization.jsx'
import Register from './body/register.jsx'
import MainWindow from './body/mainWindow.jsx';

import { BrowserRouter, Routes, Route, Outlet } from 'react-router-dom';

import LawArticles from './body/LawArticles';
import ArticleDetails from './body/ArticleDetails';

// function App() {
//   return (
//     <BrowserRouter>
//       <div>
//         <header className="head1"> 
//           <Head1 />
//         </header>
//         <div className="body1">
//           <Routes>
//             <Route path="/" element={<Body1 />}>
//               <Route index element={<Authorization />} />
//               <Route path='auth' element={<Authorization />} />
//               <Route path='reg' element={<Register />} />
//               {/* <Route path='main' element={<MainWindow />} />
//               <Route path='laws/:lawId' element={<LawArticles />} /> */}
//               <Route path='/main' element={<MainWindow />} />
//               <Route path='/api/laws/:lawId' element={<LawArticles />} />
//             </Route>
//           </Routes>
//         </div>
//       </div>
//     </BrowserRouter>
//   )
// }

function App() {
  return (
    <BrowserRouter>
      <div>
        <header className="head1"> 
          <Head1 />
        </header>
        <div className="body1">
          <Routes>
            <Route path="/" element={<Body1 />}>
              <Route index element={<Authorization />} />
              <Route path='auth' element={<Authorization />} />
              <Route path='reg' element={<Register />} />
              <Route path='main' element={<MainWindow />} />
              <Route path='laws/:lawId' element={<LawArticles />} />
              <Route path='laws/:lawId/articles' element={<LawArticles />} />
              <Route path='laws/:lawId/:articleId' element={<ArticleDetails />} />
            </Route>
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  )
}
export default App;