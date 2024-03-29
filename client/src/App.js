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
import NewGamePage from './pages/NewGamePage';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const checkToken = () => {
      const token = localStorage.getItem('token');
      console.log("check_token function");
      if (token) {
        console.log("if token")
        try {
          let jwt_token_decoded = jwtDecode(token);
          const currentTime = Date.now().valueOf() / 1000;
          if (currentTime < jwt_token_decoded.exp) {
            setIsLoggedIn(true);
            console.log("current time < jwt_token_decoded.exp ( good)");
          } else {
            console.log("current time > jwt_token_decoded.exp (bad)");
            setIsLoggedIn(false);
            localStorage.removeItem('token');
          }
        } catch (e) {
          localStorage.removeItem('token');
          setIsLoggedIn(false);
          console.log("catch");
        }
      } else {
        console.log("if not token");
        setIsLoggedIn(false);
      }
    };

    checkToken();
  }, [isLoggedIn]); 

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  console.log(localStorage.getItem('token'))
  return (
    <Router>
      <Routes>
        <Route path="/" element={isLoggedIn ? <Navigate to="/listed_games" /> : <LoginPage onLoginSuccess={handleLoginSuccess} setIsLoggedIn={setIsLoggedIn} />} />
        <Route path="/register" element={isLoggedIn ? <Navigate to="/listed_games" /> : <RegistrationPage/>} />
        <Route path="/gamepage/:gameId" element={isLoggedIn ? <GamePage setIsLoggedIn={setIsLoggedIn} /> : <Navigate to="/" />} />
        <Route path="/listed_games" element={isLoggedIn ? <ListedGamesPage setIsLoggedIn={setIsLoggedIn} /> : <Navigate to="/" />} />
        <Route path="/new_game" element={isLoggedIn ? <NewGamePage setIsLoggedIn={setIsLoggedIn} /> : <Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
