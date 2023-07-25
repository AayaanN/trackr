import logo from './logo.svg';
import './App.css';
import React, {useEffect, useState} from "react"
import {Stocks} from './components/stocks'
import {Search} from './components/search'
import GraphComponent from './components/portfolio_graph';

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
  }, [stocks]);


  return (
    <div className="App">
      <div className='mt-10 mb-10'>
        <h1 className=' flex text-6xl p-2 text-white  justify-center'>Trackr</h1>
      </div>
      
      <div className='mt-5 flex'>

        <div className='flex flex-col'>
          <Search></Search>
          <Stocks stocks={stocks} on_select_stock={set_selected_stock} selected_stock={selected_stock}/>
        </div>
        
        <div className='flex h-screen w-full'>
          <GraphComponent></GraphComponent>
        </div>
        


      </div>
  
    </div>
  );
}

export default App;
