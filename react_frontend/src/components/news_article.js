import React, { useEffect, useState } from 'react';


const NewsComponent = ({selected_stock}) => {

  // console.log('selected stock', selected_stock)

  const [news, setNews] = useState({})

  useEffect(() => {

    addNews();
    console.log('just ran addNews')
    fetch(`/get_article?selected_stock=${selected_stock}`).then(
    // fetch('/get_article').then(
      response => response.json().then(
        data => {
          setNews(data.news_article)
          // console.log( data.stock_name)
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
    <div>
        <p>{news.stock_name}</p>
        <p>{news.article_name}</p>
      Hello
    </div>
  );
};

export default NewsComponent;
