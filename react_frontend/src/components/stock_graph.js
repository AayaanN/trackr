import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { format } from 'date-fns';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);


const StockGraphComponent = ({selected_stock}) => {
    const [stockData, setStockData] = useState([]);

    const fetchStockData = async () => {
      try {
        const response = await fetch(`/get_stock_prices?stock_name=${selected_stock}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setStockData(data);
      } catch (error) {
        console.error('Error fetching stock data:', error);
      }
    };
  
    useEffect(() => {
      fetchStockData();
    }, [selected_stock]);
  
    const data = {
      labels: stockData.map((dataPoint) => dataPoint.date),
      datasets: [
        {
          label: 'Stock Prices',
          data: stockData.map((dataPoint) => dataPoint.price),
          borderColor: 'rgb(59 130 246)',
          fill: false,
        },
      ],
    };
  
    return (
      <div className='w-full'>
        {/* <h2>Stock Prices for {selected_stock}</h2> */}
        <div className='w-full content-center mx-20 rounded-lg neumorphic-shadow-2 bg-[#0C111B] text-white' style={{ width: '85%', height: '60vh' }}>
            {stockData.length > 0 ? (<Line data={data} /> ) : (<p className='text-white'>No stock data available for {selected_stock}.</p> )}
        </div>
      </div>
    );
  };
  
  export default StockGraphComponent;
  