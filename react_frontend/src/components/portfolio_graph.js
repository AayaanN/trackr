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

  useEffect(() => {
    fetchData();
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

  const formatTimeLabel = (time) => {
    // Format the time label as per your desired format
    const formattedTime = new Date(time).toISOString();
    return formattedTime;
  };

  const chartData = {
    labels: data.map(entry => formatTimeLabel(entry.time)),
    datasets: [
      {
        label: 'Value',
        data: data.map(entry => entry.value),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };

  const chartOptions = {
    maintainAspectRatio: false,
    scales: {
      x: {
        ticks: {
          callback: (value) => formatTimeLabel(value),
        },
      },
    },
  };

  return (
    <div className='h-screen'>
      {/* <h1>Graph Component</h1> */}
      <div className='w-11/12 h-11/12'>
        <Line data={chartData} options={chartOptions}/>
      </div>
    </div>
  );
};

export default GraphComponent;
