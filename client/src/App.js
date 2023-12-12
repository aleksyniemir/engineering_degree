import React, { useState } from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegistrationPage from './pages/RegistrationPage';
import GamePage from './pages/GamePage';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={isLoggedIn ? <Navigate to="/gamepage" /> : <LoginPage onLoginSuccess={handleLoginSuccess} />} />
        <Route path="/register" element={isLoggedIn ? <Navigate to="/gamepage" /> : <RegistrationPage/>} />
        <Route path="/gamepage" element={isLoggedIn ? <GamePage /> : <Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;