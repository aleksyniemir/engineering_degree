import React from 'react';
import Logout from './auth/Logout';
import './Header.css';
import { useNavigate } from 'react-router-dom';

const Header = ({ setIsLoggedIn }) => {
    const navigate = useNavigate();
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
          <Logout setIsLoggedIn={setIsLoggedIn}/>
        </header>
    );
};

export default Header;
