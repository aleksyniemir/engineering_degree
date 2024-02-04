import React from 'react';
import "../Header.css"

const Logout = ({ setIsLoggedIn }) => {
    const handleLogout = () => {
        localStorage.removeItem('token');
        setIsLoggedIn(false)
      };

  return (
    <button 
        className="header-button" 
        onClick={handleLogout}
        type="submit">
        Logout
    </button>
  );
};

export default Logout;
