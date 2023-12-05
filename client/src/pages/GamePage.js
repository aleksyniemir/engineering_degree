import React, {useState} from 'react';
import './GamePage.css'; 

function GamePage() {
    const [userInput, setUserInput] = useState('');

    return (
        <div className="game-page">
          <header className="game-header">
            <button class="ripple ripple-surface ripple-surface-light btn btn-dark mb-4"  onClick={() => {/* handle new game */}}>New game</button>
            <button class="ripple ripple-surface ripple-surface-light btn btn-dark mb-4"  onClick={() => {/* handle saved games */}}>Saved games</button>
            <button class="ripple ripple-surface ripple-surface-light btn btn-dark mb-4"  onClick={() => {/* handle logout */}}>Logout</button>
          </header>
          <main className="game-content">
            <section className="game-description">
              <p>Here goes the dynamic description of the game situation...Here goes the dynamic description of the game situation...Here goes the dynamic description of the game situation...Here goes the dynamic description of the game situation...Here goes the dynamic description of the game situation...Here goes the dynamic description of the game situation...Here goes the dynamic description of the game situation...Here goes the dynamic description of the game situation...Here goes the dynamic description of the game situation...</p>
            </section>
            <aside className="game-sidebar">
              <div className="game-photo">
                {/* Replace with dynamic content as needed */}
                <img src={require("/home/aleksyniemir/Documents/praca_inżynierska/aplikacja/client/src/example_img.png")} alt="" />
              </div>
              <div className="game-stats">
                <h2>Stats</h2>
                {/* Stats content goes here */}
              </div>
            </aside>
          </main>
          <div className="game-input"> {/* Changed from footer to div */}
                <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="Your command"
                />
            </div>
        </div>
      );

}
      export default GamePage;