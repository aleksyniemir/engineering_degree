import React from 'react';
import "../Header.css"

const Logout = ({ onLogout }) => {
    const handleLogout = () => {
        localStorage.removeItem('token');
        if (onLogout) {
          onLogout(false);
        }
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
