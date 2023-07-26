
import React, { useState, useEffect} from 'react';

export const Search = () => {
  const [query, setQuery] = useState('')
  const [amount, setAmount] = useState(0)
  const [valid, setValid] = useState(true)
  const [isErrorVisible, setErrorVisible] = useState(false)
  const [stockExists, setStockExists] = useState(false)

  const addStock = async(query, amount) => {
    await fetch('/add_data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({amount, query}),
    }).then(
      console.log(JSON.stringify({amount, query}))
    );
  }

  useEffect(() => {
    if (isErrorVisible) {
      const timeout = setTimeout(() => {
        setErrorVisible(false);
      }, 500);

      return () => clearTimeout(timeout);
    }
  }, [isErrorVisible]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {

      const check_response = await fetch('/check_stock', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })

      await check_response.json()
      .then(data => {
        setValid(data.validity)
        console.log(valid)
      })

      const added_response = await fetch('/already_added', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })

      await added_response.json()
      .then(data => {
        setStockExists(data.added)
      })


      console.log(isErrorVisible)
      if(valid===true && stockExists === false && amount !== 0){

        setErrorVisible(false)

        console.log('hello this is ion')

      // Send a POST request to the Flask endpoint using fetch
        // await fetch('/add_data', {
        //   method: 'POST',
        //   headers: {
        //     'Content-Type': 'application/json',
        //   },
        //   body: JSON.stringify({ query, amount}),
        // });

        addStock(query, amount)

        // Reset the query input
        setQuery('')
        setAmount(0)

        
      }
      else{
        setErrorVisible(true)
      }

      } catch (error) {
        console.error(error);
      }
  };

  return (
    <div className=' shadow-xl shadow-black' style={{ zIndex: '9999' , position: 'relative' }}>
      <div className='flex items-center w-36'>
            <form onSubmit={handleSubmit} className="flex items-center ">
              <input 
                type="text"
                placeholder="Add Stock"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="border border-gray-300 px-4 py-2 rounded-l-md  ml-4 w-36"
              />
              <input 
                type="text"
                placeholder="Amount"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                className="border border-gray-300 px-4 py-2 rounded-r-md mr-2 w-24"
              />
        
              <button
                type="submit"
                className="bg-blue-500 text-white px-4 py-2 rounded-md h-10"
              >
                Submit
              </button>
            
            </form>
            {isErrorVisible ? (
            <div className="flex justify-center items-center ml-2">
              <p className="text-white bg-red-500 rounded-lg w-10 h-10 flex justify-center items-center">X</p>
            </div>
          ) : null}


          </div>
    </div>
    

    
  );
};

export default Search;