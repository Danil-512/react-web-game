/*import React, { useState } from 'react'*/ /*Хуки тут не нужны вроде пока что*/
/*import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'*/ /* Это логотипы, они не нужны нам*/
import './App.css'
/*import { createRoot } from 'react-dom/client'*/ /*вот это не помню что, вроде вообще не используется*/
import Head1 from './header/head1.jsx'
import Body1 from './body/body1.jsx'

export default function App() {
  /*const [count, setCount] = useState(0)*/
  return (
    <div>
      <header id='he1' className="head1"> 
        <Head1/>
      </header>
      <div id='bo1' className="body1">
        <Body1/>
      </div>
    </div>
  )
}

/*
class Headd extends React.Component {
  render() {
    return (
      <div class='head1' id='he1'>
        {Head1.head1()}
      </div>
    );
  }
}
class Bodyy extends React.Component {
  render() {
    return (
      <div class='body1' id='bo1'>
        {Body1.body1()}
      </div>
    );
  }
}


const vdom = (
  <Heaad>
    <p>fdfd</p>
  </Heaad>
);
*/

//const rootq = ReactDOM.createRoot(document.getElementById('he1'));
//rootq.render(vdom);





//const head11 = document.getElementById('head1');
//const body11 = document.getElementById('body1');

//createRoot(head11).render(<Head1 />)
//createRoot(body11).render(<Body1 />)

  

