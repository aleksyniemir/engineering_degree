import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Logout from '../components/auth/Logout';

function NewGamePage({ setIsLoggedIn }) {
    const [inputValue, setInputValue] = useState('');
    const navigate = useNavigate();


    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };

    const handleSubmit = () => {
        // fetch('/game_page/' + inputValue)
        //     .then(() => {
        //         history.push('/game_page/' + inputValue);
        //     })
        //     .catch((error) => {
        //         console.error('Error:', error);
        //     });
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
