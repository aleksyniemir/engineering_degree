import React, {useState} from 'react';
import './GamePage.css'; 

function GamePage() {
    const [userInput, setUserInput] = useState('');

    return (
      <body class="game-page">
        <header className="game-header">
          <button class="ripple ripple-surface ripple-surface-light btn btn-dark mb-4"  onClick={() => {}}>New game</button>
          <button class="ripple ripple-surface ripple-surface-light btn btn-dark mb-4"  onClick={() => {}}>Saved games</button>
          <button class="ripple ripple-surface ripple-surface-light btn btn-dark mb-4"  onClick={() => {}}>Logout</button>
        </header>
        <div class="container">
            <div class="left-container">
                <div className="game-description">
                  <p>Here goes the dynamic description of the game situation...Here goes the dynamic description of the game situation...Here goes the dynamic description of the game situation...Here goes the dynamic description of the game situation...Here goes the dynamic description of the game situation...Here goes the dynamic description of the game situation...Here goes the dynamic description of the game situation...Here goes the dynamic description of the game situation...Here goes the dynamic description of the game situation...</p>
                </div>
              <div class="bottom-container">
                <div className="game-input"> 
                  <input
                    type="text"
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    placeholder="Your command"
                  />
                </div>
                <div className="game-photo">
                  <img src={require("/home/aleksyniemir/Documents/praca_inżynierska/aplikacja/client/src/example_img.png")} alt="" />
                </div>
              </div>
            </div>
            <div className="game-stats">
                  <h2>Stats</h2>
                </div>
            </div>
        </body>
      );

}
      export default GamePage;