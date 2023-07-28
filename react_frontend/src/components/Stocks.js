import React, {useEffect, useState} from 'react';
import { List, Header } from 'semantic-ui-react';
import './Stocks.css';



const increase = async (selected_stock) => {
  await fetch('/increase_amount', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({selected_stock}),
  });
}

const decrease = async (selected_stock) => {
  await fetch('/decrease_amount', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({selected_stock}),
  });
}

const delete_stock = async (selected_stock) => {
  
  await fetch('/delete_stock', {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({selected_stock}),
  });
}




export const Stocks = ({ stocks, on_select_stock, selected_stock }) => {

  const [value, setValue] = useState(0)

  // console.log('selected stock stocks.js', selected_stock)

  useEffect(() => {
    
    fetch('/get_portfolio').then(
      response => response.json().then(
        data => {
          setValue(data.portfolio.value)
          console.log('value:', data.portfolio.value)
        }
      )
    )
  }, [value, ])

  return (
    <div className="flex overflow-y-auto h-full">
      <ul className="space-y-1 w-80 ml-4 mt-10 mb-10">

          <button className={`flex flex-col neumorphic-shadow bg-gradient-to-r from-blue-700 to-blue-800 rounded-lg shadow-xl h-40 w-80 hover:from-blue-800 hover:to-blue-800 p-3 m-1 mb-6 ${selected_stock === 'portfolio' ? 'border-2 border-blue-500 from-blue-800 to-blue-800' : 'border-transparent border-2'}`} onClick={() => { on_select_stock('portfolio'); }}>
            <h2 className="text-2xl text-white flex-1">My Portfolio</h2>
            <p className="text-xl text-white font-medium mt-2">Value: {value.toFixed(2)}</p>

          </button>
      
        {stocks.map(stock => (
          <li key={stock.name} className="p-1">
            <button
              className={`flex flex-col bg-gray-900 rounded-lg shadow neumorphic-shadow h-30 w-80 hover:bg-[#0B1019]  p-3 mb-3 ${
                selected_stock === stock.name ? 'border-2 border-blue-500 bg-[#0B1019]' : 'border-transparent border-2'
              }`}
              onClick={() => on_select_stock(stock.name)}
            >

              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="red-400" className={`w-5 h-5 ml-[240px] mb-3 fill-gray-700 ${selected_stock === stock.name ? 'hover:fill-red-400' : 'hover:text-slate-800'}`} onClick={ async () => { await on_select_stock(stock.name); await delete_stock(selected_stock); on_select_stock('none');}}><path fillRule="evenodd" d="M16.5 4.478v.227a48.816 48.816 0 013.878.512.75.75 0 11-.256 1.478l-.209-.035-1.005 13.07a3 3 0 01-2.991 2.77H8.084a3 3 0 01-2.991-2.77L4.087 6.66l-.209.035a.75.75 0 01-.256-1.478A48.567 48.567 0 017.5 4.705v-.227c0-1.564 1.213-2.9 2.816-2.951a52.662 52.662 0 013.369 0c1.603.051 2.815 1.387 2.815 2.951zm-6.136-1.452a51.196 51.196 0 013.273 0C14.39 3.05 15 3.684 15 4.478v.113a49.488 49.488 0 00-6 0v-.113c0-.794.609-1.428 1.364-1.452zm-.355 5.945a.75.75 0 10-1.5.058l.347 9a.75.75 0 101.499-.058l-.346-9zm5.48.058a.75.75 0 10-1.498-.058l-.347 9a.75.75 0 001.5.058l.345-9z" clipRule="evenodd" /></svg>



              <div className="flex justify-center mb-2 items-center">
                <div className='flex'>
                  <h2 className="text-2xl text-white flex-1">{stock.name}</h2>
                  <p className={`ml-32 mr-5 text-4xl text-gray-600 text-bold ${selected_stock === stock.name ? 'hover:text-red-400' : 'hover:text-slate-800'}`} onClick={() => { on_select_stock(stock.name); decrease(selected_stock); }}>-</p>
                  <p className="text-2xl text-white text-semibold mt-2">{stock.amount}</p>
                  <p className={`ml-5 text-4xl text-bold text-gray-600 ${selected_stock === stock.name ? 'hover:text-green-500' : 'hover:text-slate-800'}`} onClick={() => { on_select_stock(stock.name); increase(selected_stock); }}>+</p>

                </div>

              </div>


                
             

              <div className="flex">
                <p className="text-white mb-2 font-bold mr-20 w-12">{stock.price}</p>
                <p
                  className={`text-white font-bold rounded-lg shadow-inner-md p-1 mb-3 w-36 ${
                    stock.percent_change > 0 ? 'bg-green-500' : stock.percent_change < 0 ? 'bg-red-500' : 'bg-slate-400'
                  }`}
                >
                  {stock.percent_change} %
                </p>
              </div>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};
