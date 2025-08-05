import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Head1 from './header/head1.jsx'
import Body1 from './body/body1.jsx'
import Authorization from './body/authorization.jsx'
import Register from './body/register.jsx'
import MainWindow from './body/mainWindow.jsx';
import Laws from './body/lawsUniversity/Laws.jsx'
import Article from './body/lawsUniversity/Article.jsx'
import NewArticle from './body/lawsUniversity/NewArticle.jsx'
import LawArticles from './body/lawsUniversity/LawArticles';

import './App.css'


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

              <Route path='laws' element={<Laws />} />

              <Route path='laws/:lawId' element={<LawArticles />} />

              <Route path='laws/:lawId/:articleId' element={<Article />} />

              <Route path='laws/:lawId/newArticle' element={<NewArticle />}/>
            </Route>
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  )
}

export default App;