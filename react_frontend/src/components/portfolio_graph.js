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

const GraphComponent = () => {
  const [data, setData] = useState([]);

  const [portfolioInformation, setPortfolioInformation] = useState([])

  useEffect(() => {
    fetchData();
    fetchPortfolio();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch('/graph_portfolio');
      const graphData = await response.json();
      setData(graphData);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchPortfolio = async () => {
    try {
      const response = await fetch('/get_portfolio');
      const portfolioData = await response.json();
      setPortfolioInformation(portfolioData.portfolio);
      console.log(portfolioData.portfolio, 'this is portfolio data')
    } catch (error) {
      console.error(error);
    }
  };

  const formatTimeLabel = (time) => {
    const formattedTime = time.toString().substring(0, 19);
    return formattedTime;
  };

  const chartData = {
    labels: data.map((entry) => formatTimeLabel(entry.time)),
    datasets: [
      {
        label: 'Portfolio Value',
        data: data.map((entry) => entry.value),
        borderColor: 'rgb(59 130 246)',
        tension: 0.8,
      },
    ],
  };

  const chartOptions = {
    responsive: true, // Allow responsiveness to container size
    maintainAspectRatio: false, // Override aspect ratio to set custom width and height
    scales: {
      x: {
        ticks: {
          // callback: (value) => formatTimeLabel(value),
        },
      },
    },
  };

  return (
    <div className='w-full'>
      {/* <h1>Graph Component</h1> */}
      <div className='w-full content-center mx-20 rounded-lg neumorphic-shadow-2 bg-[#0C111B] text-white' style={{ width: '85%', height: '60vh' }}>
        {/* Set width and height as per your requirement */}
        <Line data={chartData} options={chartOptions} />
      </div>
      <div className='flex inline-block mt-12'>
        
        <div className='flex flex-col'>
            <div className='flex'>
                <p className='text-white ml-24 mr-3 mb-16 font-bold text-2xl '>Portfolio Percentage Growth to Date:</p>
                <p className={` text-2xl ${portfolioInformation.percent_change > 0 ? 'text-green-500' : portfolioInformation.percent_change == 0 ? 'text-white' : 'text-red-500'}`}> {Number(portfolioInformation.percent_change).toFixed(2)} %</p>
            </div>
           
            <div className='flex'>
                <p className='text-white ml-24 mr-3 font-bold text-2xl '>Portfolio Value Increase to Date:</p>
                <p className={` text-2xl ${portfolioInformation.value > 0 ? 'text-green-500' : portfolioInformation.value == 0 ? 'text-white' : 'text-red-500'}`}> $ {Number(portfolioInformation.value).toFixed(2)} USD</p>
            </div>
           
        </div>

        <div className='flex ml-20'>
            <p className='text-white  mr-3 font-bold text-2xl'>Portfolio Actual Growth to Date:</p>
            <p className= {`text-2xl  ${portfolioInformation.change > 0 ? 'text-green-500' : portfolioInformation.change == 0 ? 'text-white' : 'text-red-500'}`}> $ {Number(portfolioInformation.change).toFixed(2)} USD</p>
        </div>
     
      </div>
    </div>
  );
};

export default GraphComponent;
