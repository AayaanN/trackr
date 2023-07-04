import React from 'react';
import { List, Header } from 'semantic-ui-react';
import './Stocks.css';


export const Stocks = ({ stocks, on_select_stock, selected_stock }) => {
  return (
    <div className=" flex overflow-y-auto h-full">
      <ul className="space-y-1 w-80 ml-4 mt-10 mb-10" >
      {stocks.map(stock => (
        <li key={stock.name} className="p-1">
          <button className={`flex flex-col bg-slate-500 rounded shadow-xl h-30 w-80 hover:bg-slate-600 p-3 ${
            selected_stock === stock.name ? 'border-2 border-blue-500 bg-slate-600' : 'border-transparent border-2 '
          }`} onClick={() => on_select_stock(stock.name)}>
            <h2 className="text-xl text-white mt-4">{stock.name}</h2>
            <div className="flex">
              <p className="text-white mb-2 font-bold mr-20">{stock.price}</p>
              <p className={`text-white font-bold  rounded-lg p-1 mb-3 w-36 ${stock.percent_change > 0 ? 'bg-green-500' : stock.percent_change < 0 ? 'bg-red-500' : 'bg-slate-400'}`}>
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
