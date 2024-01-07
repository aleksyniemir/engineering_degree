import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Logout from '../components/auth/Logout';

const NewGamePage = ({ setIsLoggedIn }) => {
    const [inputValue, setInputValue] = useState('');
    const navigate = useNavigate();
    const [gameData, setGameData] = useState({
      description: '',
      health: '',
      id: null,
      inventory: '',
      location: '',
      photo: '',
      possible_actions: '',
      quests: '',
      scene: '',
      turn_number: null,
      weather: ''
    });

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
            setGameData(data);
            console.log(`received gameData: ${gameData.id}`)
            navigate(`/gamepage/${gameData.id}`);
          }
      } catch (error) {
          console.error('Error fetching games:', error);
      }
        
    };

    return (
        <div>
            <header className="game-header">
          <button 
            className="ripple ripple-surface ripple-surface-light btn btn-dark mb-4"  
            onClick={() => navigate('/new_game')}
          >
            New game
          </button>
          <button 
            className="ripple ripple-surface ripple-surface-light btn btn-dark mb-4"  
            onClick={() => navigate('/listed_games')} 
          >
            Saved games
          </button>
          <Logout onLogout={() => setIsLoggedIn(false)} />
          </header>
            <div>
                <input type="text" value={inputValue} onChange={handleInputChange} />
                <button onClick={handleSubmit}>Submit</button>
            </div>
        </div>
    );
};

export default NewGamePage;
