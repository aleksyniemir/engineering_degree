import React, {useState} from 'react';
import './GamePage.css'; 

function GamePage() {
    const [userInput, setUserInput] = useState('');

    return (
        <div className="game-page">
          <header className="game-header">
            <button onClick={() => {/* handle new game */}}>New game</button>
            <button onClick={() => {/* handle saved games */}}>Saved games</button>
            <button onClick={() => {/* handle logout */}}>Logout</button>
          </header>
          <main className="game-content">
            <section className="game-description">
              <h2>Description of the situation</h2>
              {/* Replace this with the actual game description */}
              <p>Here goes the dynamic description of the game situation...</p>
            </section>
            <aside className="game-sidebar">
              <div className="game-photo">
                {/* Replace with dynamic content as needed */}
                <img src="path-to-your-photo.jpg" alt="Game" />
              </div>
              <div className="game-stats">
                <h2>Stats</h2>
                {/* Stats content goes here */}
              </div>
            </aside>
          </main>
          <footer className="game-input">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="User input"
            />
          </footer>
        </div>
      );

}
      export default GamePage;