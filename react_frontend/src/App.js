import logo from './logo.svg';
import './App.css';
import React, {useEffect, useState} from "react"
import {Stocks} from './components/stocks'
import {Search} from './components/search'

function App() {

  const[stocks, set_stocks] = useState([])

  const[selected_stock, set_selected_stock] = useState('')

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
      <Stocks stocks={stocks} on_select_stock={set_selected_stock} selected_stock={selected_stock}/>

    </div>
  );
}

export default App;
