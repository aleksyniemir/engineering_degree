
import './App.css';
import {useState, useEffect} from 'react'
import UserList from './components/UserList'
import Login from './components/auth/Login'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  // const [users, setUsers] = useState([])
  
  // useEffect(() => {
  //   fetch('http://localhost:5000/users/get_users', {
  //     'method': 'GET',
  //     headers: {
  //       'Content-Type': "application/json",
  //       'Authorization': `Bearer ${localStorage.getItem('token')}`
  //     }
  //   })
  //   .then(resp => resp.json())
  //   .then(resp => setUsers(resp))
  //   .catch(error => console.log(error))
  // }, [])

  
  //      <UserList users = {users}/>  
  return (
    <div className="App">
      {isLoggedIn ? ( 
        <>
          <h1> Flask and recat app</h1>
          <UserList/>
    
        </>
      ) : (
        
        <Login onLoginSuccess={handleLoginSuccess} />
      )}
    </div>
  );
}

export default App;

// import React, { useState } from 'react';
// import {
//   BrowserRouter as Router,
//   Routes,
//   Route,
//   Navigate,
// } from 'react-router-dom';
// import Login from './Login';
// import Homepage from './Homepage';

// function App() {
//   const [isLoggedIn, setIsLoggedIn] = useState(false);

//   const handleLoginSuccess = () => {
//     setIsLoggedIn(true);
//   };

//   return (
//     <Router>
//       <Routes>
//         <Route path="/" element={isLoggedIn ? <Navigate to="/homepage" /> : <Login onLoginSuccess={handleLoginSuccess} />} />
//         <Route path="/homepage" element={isLoggedIn ? <Homepage /> : <Navigate to="/" />} />
//       </Routes>
//     </Router>
//   );
// }

// export default App;

