import React from 'react';
import Logout from './auth/Logout';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

const Header = () => {
    const navigate = useNavigate();
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    return (
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
    );
};

export default Header;
