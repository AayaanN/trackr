import logo from './logo.svg';
import './App.css';
import React, {useEffect, useState} from "react"

function App() {

  useEffect(() => {
    fetch('/add_data').then(
      response => response.json().then(
        data => {
          console.log(data);
        }
      )
    )
  }


  , []) 


  return (
    <div className="App">

    </div>
  );
}

export default App;
