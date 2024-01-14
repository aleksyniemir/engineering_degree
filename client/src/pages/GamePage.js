
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
    }, [gameId]); // Dependency array to fetch game data when gameId changes

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
            <div className="left-container">
                <div className="game-description">
                  <p>{gameData.description}</p>
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
                <div className="submit-game-input">
                  <button className="ripple ripple-surface ripple-surface-light btn btn-dark mb-4" onClick={handleSubmit}>Submit</button>
                </div>
                <div className="game-photo">
                  <img src={imageSrc} alt="fetched image"/>
                </div>
              </div>
            </div>
            <div className="game-stats">
                  Turn number: {gameData.turn_number} <br></br>
                  Health: {gameData.health} <br></br>
                  Weather: {gameData.weather} <br></br>
                  Location: {gameData.location} <br></br>
                  Inventory: {gameData.inventory} <br></br>
                  Quests: {gameData.quests} <br></br>
                  Possible actions: {gameData.possible_actions} <br></br>
                </div>
            </div>
        </div>
        }
        </div>
      );

}
      export default GamePage;