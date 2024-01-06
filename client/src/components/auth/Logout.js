import React from 'react';

const Logout = ({ onLogout }) => {
    const handleLogout = () => {
        localStorage.removeItem('token');
        if (onLogout) {
          onLogout(false);
        }
      };

  return (
    <button 
        className="ripple ripple-surface ripple-surface-light btn btn-dark mb-4" 
        onClick={handleLogout}
        type="submit">
        Logout
    </button>
  );
};

export default Logout;
