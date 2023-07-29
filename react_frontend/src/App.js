import logo from './logo.svg';
import './App.css';
import React, {useEffect, useState} from "react"
import {Stocks} from './components/stocks'
import {Search} from './components/search'
import GraphComponent from './components/portfolio_graph';
import NewsComponent from './components/news_article';

function App() {

  const[stocks, set_stocks] = useState([])

  const[selected_stock, set_selected_stock] = useState('portfolio')

  // const submitTemp = () => {

  //   fetch('/add_data', {
  //     method: 'POST',
  //     headers: {'Content-Type': 'application/json'},
  //   }).then( () => {
  //     console.log('temp added')
  //   })
  // }

  // console.log(selected_stock)

  useEffect(() => {
    fetch("/get_data").then(response =>
      response.json().then(data => {
        set_stocks(data.stocks);
      })
    );
  }, [stocks]);


  return (
    <div className="App min-h-screen ">

      
      <div className='mt-5 flex flex-col h-full'>

        <div className='h-[calc(100%/7)]'>
          <h1 className=' flex text-6xl p-2 text-white justify-center'>Trackr</h1>
        </div>

        <div className='flex h-[calc(600%/7)]'>

          <div className='flex flex-col  h-full'>
            <div>
              <Search></Search>
            </div>
      
            <div className=' h-full w-96 overflow-y-auto'>
              <Stocks stocks={stocks} on_select_stock={set_selected_stock} selected_stock={selected_stock}/>
            </div>
            
          </div>
          
          <div className='flex h-full w-full flex-col '>
            
            {selected_stock === 'portfolio' ? <GraphComponent></GraphComponent> : null}

            {(selected_stock === 'portfolio' || selected_stock === 'none') ? null : <NewsComponent selected_stock={selected_stock}></NewsComponent>}
      
          </div>

        </div>

        <div>
          <p className='text-gray-600 border-2 border-gray-900'>Aayaan Naqvi and Ernest Wang, 2023</p>
        </div>

      </div>
  
    </div>
  );
}

export default App;
