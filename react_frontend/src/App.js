import logo from './logo.svg';
import './App.css';
import React, {useEffect, useState} from "react"
import {Stocks} from './components/stocks'
import {Search} from './components/search'

function App() {

  const[stocks, set_stocks] = useState([])

  const[random_temp, set_random_temp] = useState(0)

  // const submitTemp = () => {

  //   fetch('/add_data', {
  //     method: 'POST',
  //     headers: {'Content-Type': 'application/json'},
  //   }).then( () => {
  //     console.log('temp added')
  //   })
  // }


  useEffect(() => {
    fetch("/get_data").then(response =>
      response.json().then(data => {
        set_stocks(data.stocks);
      })
    );
  }, []);


  return (
    <div className="App">
      <h1 className='text-6xl p-2 text-white mt-4'>Trackr</h1>

      <Search></Search>
      <Stocks stocks={stocks} />

    </div>
  );
}

export default App;
