import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';



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
                setGames(data);
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
            <h1>Listed Games</h1>
            <ul>
                {games.map((game) => (
                    <div key={game.id}>Title: {game.title},  {game.id},   Turn number: {game.turn_number}
                    <button className="ripple ripple-surface ripple-surface-light btn btn-dark mb-4"
                        onClick={() => goToGamePage(game.id)}>     
                        Load game
                    </button>
                    <button className="ripple ripple-surface ripple-surface-light btn btn-dark mb-4"
                        onClick={() => removeGame(game.id)}>     
                        Remove game
                    </button>   
                    </div>
                ))};
            </ul>
        </div>
    );
};

export default ListedGamesPage;
