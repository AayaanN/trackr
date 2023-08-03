import React, { useEffect, useState } from 'react';


const NewsComponent = ({selected_stock}) => {

  // console.log('selected stock', selected_stock)

  const [news, setNews] = useState({})

  useEffect(() => {

    addNews();
    // console.log('just ran addNews')
    fetch(`/get_article?selected_stock=${selected_stock}`).then(
    // fetch('/get_article').then(
      response => response.json().then(
        data => {
          setNews(data.news_article)
          // console.log('time', data)
        }
      )
    )
  }, [selected_stock])

  // useEffect(() => {

  //     addNews();
  //   }, [selected_stock]);

    const addNews = async () => {

      try{
          const response = await fetch('/add_article', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({selected_stock})
          });
      }
      catch(error){
          console.error(error);
      }

    }


  return (
    <div className='w-full mt-8'>
      
      <a href={news.url} target="_blank" rel="noopener noreferrer" >
        <div className='flex neumorphic-shadow rounded-xl bg-gray-900 w-5/6 h-24 mx-24 hover:bg-[#0B1019] '>
          <img src={news.image} className='rounded-xl h-16 w-16 shadow-lg shadow-gray-950 object-cover m-4'></img>
          <div className='flex flex-col m-3'>
            <div className='flex'>
              <p className='text-blue-600 font-semibold text-lg mr-8 w-68'>{news.publisher_name}</p>
              <p className='text-blue-400 font-normal text-lg'>{news.time}</p>
            </div>
    
            <p className='text-white font-medium text-lg'>{news.article_name}</p>
          </div>
          
        </div>
        
      </a>
    </div>
  );
};

export default NewsComponent;
