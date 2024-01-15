import React from 'react';
import Logout from './auth/Logout';
import './Header.css';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

const Header = () => {
    const navigate = useNavigate();
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    return (
        <header className="game-header">
          <button 
            className="header-button"  
            onClick={() => navigate('/new_game')}
          >
            New game
          </button>
          <button 
            className="header-button"  
            onClick={() => navigate('/listed_games')} 
          >
            Games
          </button>
          <Logout onLogout={() => setIsLoggedIn(false)} />
        </header>
    );
};

export default Header;
