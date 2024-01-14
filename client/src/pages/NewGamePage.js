import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Header from '../components/Header';

const NewGamePage = () => {
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };

    const handleSubmit = async () => {
        if (!inputValue) {
            alert('Input cannot be empty');
            return;
        }
        setLoading(true);
        try {
          const response = await fetch('http://localhost:5000/gpt/begin_game', {
          method: 'POST',
          headers: { 
              'Content-Type': 'application/json', 
              'Authorization': 'Bearer ' + localStorage.getItem('token')
          },
          body: JSON.stringify({ game_environment: inputValue })
          });
          const data = await response.json();
          console.log(data);
          if (!data || Object.keys(data).length === 0) {
            alert('Game could not load properly.');
            console.log(`Did not receive gameData: ${data.id}`)
            navigate('/listed_games');
          } else {
            console.log(`received gameData: ${data.id}`)
            navigate(`/gamepage/${data.id}`);
          }
      } catch (error) {
          console.error('Error fetching games:', error);
      } finally {
          setLoading(false);
      }
        
    };

    return (
        <div>
            {isLoading ? "" : 
            (<Header/>)}
            
            <div>
                {isLoading ? "" : 
                (<input type="text" value={inputValue} onChange={handleInputChange} />)}
                {isLoading ? "" : 
                (<button onClick={handleSubmit}>Submit</button>)}
                {isLoading ? 
                    <div style={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '100vh'
                      }}>
                        <img style={{width:"200px", height:"200px"}} src="spinner.gif"/> 
                    </div>: ""}    
            </div>
        </div>
    );
};

export default NewGamePage;
