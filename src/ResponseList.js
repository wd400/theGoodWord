
import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Typography from '@mui/material/Typography';

export default function ResponseList({words,lang}) {
    //create a new array by filtering the original array

    /*
    return (
        <ul>
            {words.map((item) => (

                <li>
                    <p>{item[1]}</p>
                    <p>{item[0]}</p>
                </li>
            ))}
        </ul>
    )
    */

    return (

        <List sx={{ width: '70%',  bgcolor: 'background.paper' }}>

{words.map((item) => (
        <ListItem alignItems="flex-start" button component="a" href={"https://"+lang+".wiktionary.org/wiki/"+item[0]} target="_blank">
  
  
          <ListItemText
            primary={item[0]}
            secondary={
              <React.Fragment>
                <Typography
                  sx={{ display: 'inline' }}
                  component="span"
                  variant="body2"
                  color="text.primary"
                >
                  {item[1]}
                </Typography>
              </React.Fragment>
            }
          />
        </ListItem>

))}
     
      </List>

    )
}

