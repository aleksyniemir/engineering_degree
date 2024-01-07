import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Header from '../components/Header';

const NewGamePage = () => {
    const [inputValue, setInputValue] = useState('');
    const navigate = useNavigate();

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };

    const handleSubmit = async () => {
        if (!inputValue) {
            alert('Input cannot be empty');
            return;
        }
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
      }
        
    };

    return (
        <div>
            <Header/>
            <div>
                <input type="text" value={inputValue} onChange={handleInputChange} />
                <button onClick={handleSubmit}>Submit</button>
            </div>
        </div>
    );
};

export default NewGamePage;
