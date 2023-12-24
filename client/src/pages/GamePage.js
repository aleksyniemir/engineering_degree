import React, {useState} from 'react';
import './GamePage.css'; 

function GamePage() {
    const [userInput, setUserInput] = useState('');

    return (
      <div>
      <div className="game-page">
        <header className="game-header">
          <button class="ripple ripple-surface ripple-surface-light btn btn-dark mb-4"  onClick={() => {}}>New game</button>
          <button class="ripple ripple-surface ripple-surface-light btn btn-dark mb-4"  onClick={() => {}}>Saved games</button>
          <button class="ripple ripple-surface ripple-surface-light btn btn-dark mb-4"  onClick={() => {}}>Logout</button>
        </header>
        <div class="container">
            <div class="left-container">
                <div className="game-description">
                  <p>Welcome to the world of Dune! You find yourself on the desert planet Arrakis, known as the only source of the invaluable spice melange in the universe. As a brave adventurer, your goal is to survive and thrive in this harsh and treacherous environment, navigating the political intrigue and fierce battles for control of the spice. Be cautious, for danger lurks around every corner, but riches and power also await those who can seize the opportunities presented to them.</p>              </div>
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
                  <img src={require("/home/aleksyniemir/Documents/studies/praca_inżynierska/aplikacja/client/src/example_img.png")} alt="" />
                </div>
              </div>
            </div>
            <div className="game-stats">
                  
                  "Health": "20/20" <br></br>
                  "Weather": "Hot and dry" <br></br>
                  "Location": "Arrakis" <br></br>
                  "Inventory": "Nothing" <br></br>
                  "Quests": "None" <br></br>
                  "Possible actions": <br></br>
                  ["Explore the nearby spice mining operations"<br></br> "Search for a group of Fremen to join"<br></br> "Find shelter from the relentless sun"]
                </div>
            </div>
        </div>
        </div>
      );

}
      export default GamePage;