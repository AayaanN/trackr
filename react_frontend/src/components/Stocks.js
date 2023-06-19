import React from 'react';
import { List, Header } from 'semantic-ui-react';
import './Stocks.css';

export const Stocks = ({ stocks }) => {
  return (
    
    <List className='stock-list'>
      {stocks.map(stock => (
        <List.Item key={stock.name}>
          <div className='stock-item'>
            <Header>{stock.name}</Header>
            <p className='price'>{stock.price}</p>
          </div>
        </List.Item>
      ))}
    </List>
  );
};
