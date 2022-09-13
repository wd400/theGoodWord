
import TextField from "@mui/material/TextField";
import './App.css';
import ResponseList from "./ResponseList";
import { React,  useState } from 'react'

import Divider from '@mui/material/Divider';
function App() {


  const [wordList, setWordList] = useState([]);

  let getWords = (definition) => {
    //convert input text to lower case
 fetch('http://127.0.0.1:8000',{
      method: 'POST',
      body: JSON.stringify({
        definition:definition
      }),
      headers: {
        'Content-type': 'application/json;',
      }
      }).then(function(response){ 
        return response.json()})
        .then(function(data)
        {
          setWordList(data)

      }).catch(error => console.error('Error:', error))

  }




  return (
    <div className="App">
      <header className="App-header">
        <h1>Le bon mot</h1>
        <h6>Trouvez un mot à partir de sa définition (approximative)</h6>


      <div className="search">
        <TextField
          id="outlined-basic"
          variant="outlined"
          fullWidth
          label="Search"

          onKeyPress={(ev) => {
            if (ev.key === 'Enter') {
              // Do code here
              getWords(ev.target.value)
              ev.preventDefault();
            }
          }}


          size="small"
          inputProps={{ maxLength: 200 }}          
        />
      </div>
      <Divider variant="inset" component="li" />
      { wordList.length>0 &&
        <ResponseList words={wordList}  />
      } 
      
      </header>
      
    </div>
  );
}

export default App;
