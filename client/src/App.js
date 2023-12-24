import React, { useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegistrationPage from './pages/RegistrationPage';
import GamePage from './pages/GamePage';
import ListedGamesPage from './pages/ListedGamesPage';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const checkToken = () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          let jwt_token_decoded = jwtDecode(token);
          const currentTime = Date.now().valueOf() / 1000;
          if (currentTime > jwt_token_decoded.exp) {
            setIsLoggedIn(false);
            localStorage.removeItem('token');
          } else {
            setIsLoggedIn(true);
          }
        } catch (e) {
          // handle any errors, such as invalid token
          setIsLoggedIn(false);
          localStorage.removeItem('token');
        }
      }
    };

    checkToken();
  }, [isLoggedIn]);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={isLoggedIn ? <Navigate to="/listed_games" /> : <LoginPage onLoginSuccess={handleLoginSuccess} />} />
        <Route path="/register" element={isLoggedIn ? <Navigate to="/listed_games" /> : <RegistrationPage />} />
        <Route path="/gamepage" element={isLoggedIn ? <GamePage /> : <Navigate to="/" />} />
        <Route path="/listed_games" element={isLoggedIn ? <ListedGamesPage /> : <Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
