import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import './ListedGamesPage.css';


const ListedGamesPage = ({ setIsLoggedIn }) => {
    const [games, setGames] = useState([]);
    const navigate = useNavigate();
    
    useEffect(() => {
        const fetchGames = async () => {
            try {
                const response = await fetch('http://localhost:5000/gpt/listed_games', {
                method: 'GET',
                headers: { 
                    'Content-Type': 'application/json', 
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                },
                });
                const data = await response.json();
                if (!data || Object.keys(data).length === 0) {
                    setGames([]);
                } else {
                    const sortedGames = data.sort((a, b) => a.id - b.id);
                    setGames(sortedGames);
                }
            } catch (error) {
                console.error('Error fetching games:', error);
            }
        };

        fetchGames();
    }, []);

    const goToGamePage = (gameId) => {
        console.log(`/gamepage/${gameId}`)
        navigate(`/gamepage/${gameId}`);
    };

    const removeGame = async (gameId) => {
        try {
            const response = await fetch(`http://localhost:5000/gpt/remove_game/${gameId}`, {
            method: 'DELETE',
            headers: { 
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            });
            const data = await response.json();
            console.log(data);
            if (!data || Object.keys(data).length === 0) {
                alert('Game could not be removed.');
                navigate('/listed_games');
            } else {
                alert('Game removed.');
                navigate('/listed_games');
            }
        } catch (error) {
            console.error('Error removing game:', error);
        }
    }

    return (
        <div>
            <Header/>
            <div className="table-container">
                <table>
                <thead>
                    <tr>
                    <th>#</th>
                    <th>Title</th>
                    <th>Turn Number</th>
                    <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {games.map((game, index) => (
                    <tr key={game.id}>
                        <td>{index + 1}</td>
                        <td>{game.title}</td>
                        <td>{game.turn_number}</td>
                        <td>
                        <button className="listed-game-load-button" onClick={() => goToGamePage(game.id)}>
                            Load game
                        </button>
                        <button className="listed-game-remove-button" onClick={() => removeGame(game.id)}>
                            Remove game
                        </button>
                        </td>
                    </tr>
                    ))}
                </tbody>
                </table>
            </div>
        </div>
    );
};

export default ListedGamesPage;
