import React from 'react';
import { List, Header } from 'semantic-ui-react';
import './Stocks.css';

export const Stocks = ({ stocks, on_select_stock, selected_stock}) => {
  return (
    
    <ul className="space-y-1 w-80 ml-4 mt-16">
  {stocks.map(stock => (
      <li key={stock.name} className="p-1">
        <button className={`bg-slate-500 rounded shadow h-30 w-80 hover:bg-slate-600 p-3 ${
              selected_stock === stock.name ? 'border-2 border-blue-500' : 'border-transparent border-2'
            }`} onClick={() => on_select_stock(stock.name)}>
          <h2 className="text-xl text-white mt-4">{stock.name}</h2>
          <p className="text-white mb-10">{stock.price}</p>
        </button>
      </li>
  ))}
</ul>
  );
};
