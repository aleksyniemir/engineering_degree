
import React, {useEffect, useState} from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './GamePage.css'; 
import Header from '../components/Header';



function GamePage({ setIsLoggedIn }) {
    const [userInput, setUserInput] = useState('');
    const { gameId } = useParams();
    const [isLoading, setLoading] = useState(false);
    const navigate = useNavigate();
    var [imageSrc, setImageSrc] = useState(''); 
    const [gameData, setGameData] = useState({
      description: '',
      health: '',
      id: null,
      inventory: '',
      location: '',
      photo: '',
      possible_actions: '',
      quests: '',
      scene: '',
      turn_number: null,
      weather: ''
    });
    

    useEffect( () => {
      const fetchGame = async () => {
        try {
          const response = await fetch(`http://localhost:5000/gpt/get_game/${gameId}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + localStorage.getItem('token')
            }
          });
          const data = await response.json();
          console.log(data);
          if (!data || Object.keys(data).length === 0) {
            alert('Game could not load properly.');
            navigate('/listed_games');
          } else {
            setGameData(data);
            setImageSrc(`data:image/png;base64,${data.photo}`);
            console.log(imageSrc);
          }
        } catch (error) {
          console.error('Error fetching game:', error);
        }
      }
      fetchGame();
    }, [gameId]);

    const handleSubmit = async (event) => {
      event.preventDefault();
      if (!userInput) {
        alert('Input cannot be empty');
        return;
      }
      setLoading(true);
      try {
        const response = await fetch(`http://localhost:5000/gpt/get_next_turn/${gameId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          },
          body: JSON.stringify({ input: userInput }),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log(data);
        if (!data || Object.keys(data).length === 0) {
          alert('Game could not load properly.');
          navigate('/listed_games');
        } else {
          setGameData(data);
          setImageSrc(`data:image/png;base64,${data.photo}`);
          setUserInput('');
        }

      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false);
    }
    };

    return (
      <div>
      {isLoading ? 
                    <div style={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '100vh' 
                      }}>
                        <img style={{width:"200px", height:"200px"}} src="/spinner.gif" /> 
                    </div>
      : 
        <div className="game-page">
          <Header/>
          <div className="container">
          
            <div className="upper-container">
              <div className="game-description">
                <p>{gameData.description}</p>
              </div>
            </div>
          
            <div className="middle-container">
              <div className="game-photo">
                  <img src={imageSrc} alt="fetched image"/>
              </div>
              <div className="game-stats">
                Turn number: {gameData.turn_number} <br/>
                Health: {gameData.health} <br/>
                Weather: {gameData.weather} <br/>
                Location: {gameData.location} <br/>
                Inventory: {gameData.inventory} <br/>
                Quests: {gameData.quests} <br/>
                Possible actions: <br/>
                {
                  gameData.possible_actions.slice(1, -1)
                  .slice(1, -1)
                  .split("', '") 
                  .map((action, index) => (
                    <div key={index}>- {action}</div> 
                  ))
                }
              </div>
            </div>
            
            <div className="bottom-container">
              <div className="game-input"> 
                <input
                  type="text"
                  value={userInput}
                  onChange={(e) => setUserInput(e.target.value)}
                  placeholder="Your command"
                  />
              </div>
              <button className="submit-turn-button" onClick={handleSubmit}>Submit</button>
            </div>
          </div>
        </div>
        }
      </div>
      );
            
}
      export default GamePage;