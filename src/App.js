
import TextField from "@mui/material/TextField";
import './App.css';
import ResponseList from "./ResponseList";
import { React,  useState } from 'react'

import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';

import SVGComponent from './LoadingLogo'

function App() {


  const [wordList, setWordList] = useState([]);
  const [lang, setLang] = useState("fr");
  const [loading, setLoading] = useState(false);

  let getWords = (definition) => {

    setWordList([])
    //convert input text to lower case
 fetch('https://cfcb-81-64-42-202.eu.ngrok.io/tgw',{
      method: 'POST',
      body: JSON.stringify({
        definition:definition,
        lang:lang
      }),
      headers: {
        'Content-type': 'application/json;',
      }
      }).then(function(response){ 
        return response.json()})
        .then(function(data)
        {
          setLoading(false)
          setWordList(data)

      }).catch(error =>  setLoading(false))
      
  }




  return (
    <div className="App">
      <header className="App-header">
        <h1>Le bon mot</h1>
        <h5>Trouvez un mot à partir de sa définition (approximative)
        <br/>
          Find a word from its (approximate) definition
        </h5>



        <RadioGroup
    defaultValue="fr"

    row
    value={lang}
    onChange={(e)=>{
      setWordList([])
setLang(e.target.value)

    }}
  >
    <FormControlLabel value="fr" control={<Radio />} label="🇫🇷" />
    <FormControlLabel value="en" control={<Radio />} label="🇺🇸" />
  </RadioGroup>


      <div className="search">
        <TextField
          id="outlined-basic"
          variant="outlined"
          fullWidth
          label="Search"

          onKeyPress={(ev) => {
            if (ev.key === 'Enter') {
              // Do code here
              if (loading){
                return
              }
              setLoading(true)
              getWords(ev.target.value)
             
              console.log("0")
              ev.preventDefault();
            }
          }}


          size="small"
          inputProps={{ maxLength: 200 }}          
        />
      </div>
   {loading &&  <SVGComponent  style={{  position: 'absolute' }}/>}  

    

      { wordList.length>0 &&
        <ResponseList words={wordList} lang={lang} />
      } 
      
      </header>
      
    </div>
  );
}

export default App;
