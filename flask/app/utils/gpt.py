import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from app.schemas.game import game_create_schema, game_update_schema

load_dotenv()



def initialize_gpt_client():
  client = OpenAI(
      organization="org-M3Ibgl6TbM8lwc9aKuANBNsz",
      api_key = os.getenv("OPENAI_API_KEY")
  ) 
  return client

#The game must use the world from Frank Herbert's Dune. The game can start on any of the planets from the series.
def generate_game(user_id: int, game_environment: str):
  client = initialize_gpt_client()
  
  prompt = '''
  You are a computer program which imitates a game master, designed to output only JSON file:
  ```
  {
  "Description": "X",
  "Scene": "X",
  "Health": "X/20",
  "Weather": "X",
  "Location": "X",
  "Inventory": "X",
  "Quests": "X",
  "Possible actions": "X",
  }
  ```

  Follow the rules below.
  Main rules:
  1. Play the game in turns, starting with you.
  2. Always wait for the user to give you a response.
  3. Replace every "X" in the output with text.
  4. 'Description' must stay between 3 to 10 sentences.
  5. 'Scene' is a one sentence description of the things that the player sees based on description.
  6. 'Health' is a number from 0 to 20. The player starts with 20. If it reaches 0 or below, the player dies and the game is over (He can start the game again. Game must write completly different story). The player can lose all of his health and die by doing risky stuff. The player can gain health by eating, drinking, or sleeping. 
  7. 'Weather' and 'Location' is dependent on the description.
  8. 'Inventory' is a list of items that the player has. The player can gain items by picking them up or by buying them. The player can lose items by dropping them or by selling them. The player can use items by eating them, drinking them, or by using them. The player can only use items that he has in his inventory.
  9. 'Quests' can be created by the game or can be gained from talking to people.
  10. 'Possible actions' are representing what the player can do next. Every action should be very short. There should be three possible actions. It must be a list.

  Rules for creation of the world and the setting:
  1. {game_environment}
  2. The game must end in an exciting manner when the game decides that it is the time for the end. When the game is over, inform the player about it in the description. The player can continue playing if he wishes to.

  Start the game.
  '''

  # completion = client.chat.completions.create(
  #   model="gpt-3.5-turbo",
  #   messages=[
  #     {"role": "system", "content": prompt}
  #     ]
  # )
  game = {
    'Description': 'You are a brave adventurer who has arrived on the desert planet of Arrakis, also known as Dune. The planet is known for its harsh and inhospitable conditions, with towering sand dunes and scorching heat. You have come to this unforgiving world in search of the valuable resource known as spice, which is found only on Arrakis. Spice is highly sought after and can be used for a variety of purposes, including interstellar travel and extending life. As you step out of your ship and onto the sandy surface of Dune, you take a moment to absorb the vastness of the desert before you.', 
    'Scene': 'The sun beats down relentlessly, casting long shadows across the shifting sand dunes. The wind howls, carrying with it the sound of sand grains swirling and scraping against each other.', 
    'Health': '20/20', 
    'Weather': 'Hot and dry', 
    'Location': 'Arrakis (Dune)', 
    'Inventory': 'Empty', 
    'Quests': 'None', 
    'Possible actions': 'Explore the surroundings, look for a settlement, search for water'}
  #first_turn = json.loads(completion.choices[0].message.content)
  game["user_id"] = user_id
  game["title"] = game_environment
  game["prompt"] = prompt
  game["turn_number"] = 1
  return game



#print(completion.choices[0].message)

# completion.choices[0].message.content
# '{\n"Description": "You are a brave adventurer who has arrived on the desert planet of Arrakis, also known as Dune. The planet is known for its harsh and inhospitable conditions, with towering sand dunes and scorching heat. You have come to this unforgiving world in search of the valuable resource known as spice, which is found only on Arrakis. Spice is highly sought after and can be used for a variety of purposes, including interstellar travel and extending life. As you step out of your ship and onto the sandy surface of Dune, you take a moment to absorb the vastness of the desert before you.",\n"Scene": "The sun beats down relentlessly, casting long shadows across the shifting sand dunes. The wind howls, carrying with it the sound of sand grains swirling and scraping against each other.",\n"Health": "20/20",\n"Weather": "Hot and dry",\n"Location": "Arrakis (Dune)",\n"Inventory": "Empty",\n"Quests": "None",\n"Possible actions": "Explore the surroundings, look for a settlement, search for water"\n}'

#json
# {'Description': 'You are a brave adventurer who has arrived on the desert planet of Arrakis, also known as Dune. The planet is known for its harsh and inhospitable conditions, with towering sand dunes and scorching heat. You have come to this unforgiving world in search of the valuable resource known as spice, which is found only on Arrakis. Spice is highly sought after and can be used for a variety of purposes, including interstellar travel and extending life. As you step out of your ship and onto the sandy surface of Dune, you take a moment to absorb the vastness of the desert before you.', 'Scene': 'The sun beats down relentlessly, casting long shadows across the shifting sand dunes. The wind howls, carrying with it the sound of sand grains swirling and scraping against each other.', 'Health': '20/20', 'Weather': 'Hot and dry', 'Location': 'Arrakis (Dune)', 'Inventory': 'Empty', 'Quests': 'None', 'Possible actions': 'Explore the surroundings, look for a settlement, search for water'}

# completion_1 = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": prompt},
#     {"role": "assistant", "content": '{\n"Description": "You are a brave adventurer who has arrived on the desert planet of Arrakis, also known as Dune. The planet is known for its harsh and inhospitable conditions, with towering sand dunes and scorching heat. You have come to this unforgiving world in search of the valuable resource known as spice, which is found only on Arrakis. Spice is highly sought after and can be used for a variety of purposes, including interstellar travel and extending life. As you step out of your ship and onto the sandy surface of Dune, you take a moment to absorb the vastness of the desert before you.",\n"Scene": "The sun beats down relentlessly, casting long shadows across the shifting sand dunes. The wind howls, carrying with it the sound of sand grains swirling and scraping against each other.",\n"Health": "20/20",\n"Weather": "Hot and dry",\n"Location": "Arrakis (Dune)",\n"Inventory": "Empty",\n"Quests": "None",\n"Possible actions": "Explore the surroundings, look for a settlement, search for water"\n}'},
#     {"role": "user", "content": "try to find a sand worm"}
#     ]
# )

# '{\n"Description": "As you set out to find a sand worm on the desert planet of Arrakis, you brace yourself for the dangerous task ahead. Sand worms are massive creatures that burrow deep within the desert sands, and they are the source of much fear and fascination among the inhabitants of Dune. These colossal creatures can reach incredible sizes, with some measuring hundreds of meters in length. As you venture deeper into the desert, you keep your senses alert, hoping to catch a glimpse of one of these legendary creatures.",\n"Scene": "You find yourself surrounded by endless rolling sand dunes, their golden hues shifting and shimmering in the harsh sunlight. The wind carries the faint sound of distant rumbling beneath the surface, hinting at the presence of the mighty sand worms.",\n"Health": "20/20",\n"Weather": "Hot and dry",\n"Location": "Arrakis (Dune)",\n"Inventory": "Empty",\n"Quests": "None",\n"Possible actions": "Continue exploring, search for worm tracks, create vibrations to attract a sand worm"\n}'
# {'Description': 'As you set out to find a sand worm on the desert planet of Arrakis, you brace yourself for the dangerous task ahead. Sand worms are massive creatures that burrow deep within the desert sands, and they are the source of much fear and fascination among the inhabitants of Dune. These colossal creatures can reach incredible sizes, with some measuring hundreds of meters in length. As you venture deeper into the desert, you keep your senses alert, hoping to catch a glimpse of one of these legendary creatures.', 'Scene': 'You find yourself surrounded by endless rolling sand dunes, their golden hues shifting and shimmering in the harsh sunlight. The wind carries the faint sound of distant rumbling beneath the surface, hinting at the presence of the mighty sand worms.', 'Health': '20/20', 'Weather': 'Hot and dry', 'Location': 'Arrakis (Dune)', 'Inventory': 'Empty', 'Quests': 'None', 'Possible actions': 'Continue exploring, search for worm tracks, create vibrations to attract a sand worm'}