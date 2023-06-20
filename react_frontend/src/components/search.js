import React, { useState } from 'react';

export const Search = () => {
  const [query, setQuery] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Send a POST request to the Flask endpoint using fetch
      await fetch('/add_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      // Reset the query input
      setQuery('');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center">
      <input 
        type="text"
        placeholder="Add Stock"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="border border-gray-300 px-4 py-2 rounded-md mr-2 ml-4 w-60"
      />
      <button
        type="submit"
        className="bg-blue-500 text-white px-4 py-2 rounded-md"
      >
        Submit
      </button>
    </form>
  );
};

export default Search;
