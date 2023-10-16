
import './App.css';
import {useState, useEffect} from 'react'
import UserList from './components/UserList'
import Login from './components/Login'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  const [users, setUsers] = useState([])
  
  useEffect(() => {
    fetch('http://127.0.0.1:5000/get_users', {
      'method': 'GET',
      headers: {
        'Content-Type': "application/json"
      }
    })
    .then(resp => resp.json())
    .then(resp => setUsers(resp))
    .catch(error => console.log(error))
  }, [])
  
  return (
    <div className="App">
      {isLoggedIn ? ( 
        <>
          <h1> Flask and recat app</h1>
          <UserList users = {users}/>
        </>
      ) : (
        <Login onLoginSuccess={handleLoginSuccess} />
      )}
    </div>
  );
}

export default App;
