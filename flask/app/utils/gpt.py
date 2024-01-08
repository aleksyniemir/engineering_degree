import os
import json
import base64
from openai import OpenAI
from dotenv import load_dotenv
from app.schemas.game import game_schema_create, game_schema_update
from marshmallow import ValidationError

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
  
  prompt = f'''
  You are a computer program which imitates a game master, designed to output only JSON file:
  {{
  "description": "X",
  "scene": "X",
  "health": "X/20",
  "weather": "X",
  "location": "X",
  "inventory": "X",
  "quests": "X",
  "possible_actions": "X",
  }}

  The world is set in this universum: {game_environment} .
  Create the description in the environment above.
  
  Follow the rules below.
  1. Play the game in turns, starting with you.
  2. Always wait for the user to give you a response.
  3. Replace every "X" in the output with text.
  4. 'description' must stay between 3 to 10 sentences.
  5. 'scene' is a one sentence description of the things that the player sees based on description.
  6. 'health' is a number from 0 to 20. The player starts with 20. If it reaches 0 or below, the player dies and the game is over (He can start the game again. Game must write completly different story). The player can lose all of his health and die by doing risky stuff. The player can gain health by eating, drinking, or sleeping. 
  7. 'weather' and 'Location' is dependent on the description.
  8. 'location' is just a name of the place where the player is. 
  9. 'inventory' is a list of items that the player has. The player can gain items by picking them up or by buying them. The player can lose items by dropping them or by selling them. The player can use items by eating them, drinking them, or by using them. The player can only use items that he has in his inventory. If empty, write 'None'.
  10. 'quests' can be created by the game or can be gained from talking to people. If empty, write 'None'.
  11. 'possible_actions' are representing what the player can do next. Every action should be very short. There should be three possible actions. It must be a string.

  Start the game.
  '''

  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": prompt}
      ]
  )
  game = json.loads(completion.choices[0].message.content)
  game["user_id"] = user_id
  game["title"] = game_environment
  game["prompt"] = prompt
  game["turn_number"] = 1
  game['photo'] = b'\x00\x01\x02\x03'

  # MOCK DATA z palca
  # game = {
  #   'description': 'You are a brave adventurer who has arrived on the desert planet of Arrakis, also known as Dune. The planet is known for its harsh and inhospitable conditions, with towering sand dunes and scorching heat. You have come to this unforgiving world in search of the valuable resource known as spice, which is found only on Arrakis. Spice is highly sought after and can be used for a variety of purposes, including interstellar travel and extending life. As you step out of your ship and onto the sandy surface of Dune, you take a moment to absorb the vastness of the desert before you.', 
  #   'scene': 'The sun beats down relentlessly, casting long shadows across the shifting sand dunes. The wind howls, carrying with it the sound of sand grains swirling and scraping against each other.', 
  #   'health': '20/20', 
  #   'weather': 'Hot and dry', 
  #   'location': 'Arrakis (Dune)', 
  #   'inventory': 'Empty', 
  #   'quests': 'None', 
  #   'possible_actions': 'Explore the surroundings, look for a settlement, search for water',
  #   "user_id": user_id, 
  #   "title": game_environment,
  #   "prompt": prompt,
  #   "turn_number": 1,
  #   'photo': b'\x00\x01\x02\x03'
  #   }

  # MOCK DATA real
  # game = {
  # 'description': "Welcome to the world of fantasy! In this magical kingdom of Elvoria, you find yourself surrounded by lush green landscapes, towering mountains, and mystical creatures. The air is filled with the sweet fragrance of blooming flowers and the gentle melody of birds chirping. As you explore the enchanting forests, you stumble upon a hidden trail leading to a secret waterfall. The cascading water shimmers under the sun's rays, creating a magical spectacle. You feel the rejuvenating mist on your skin and the peacefulness of the surroundings embrace you. Your adventure in Elvoria begins...",
  # 'scene': 'You are standing in a serene forest, mesmerized by the beauty of the hidden waterfall.',
  # 'health': '20/20',
  # 'weather':  'Sunny',
  # 'location': 'Enchanted Forest',
  # 'inventory': 'None',
  # 'quests': 'None',
  # 'possible_actions': '1. Explore the forest. 2. Approach the waterfall. 3. Look for hidden treasures.',
  # 'user_id': 1,
  # 'title': 'harry potter',
  # 'prompt': prompt,
  # 'turn_number': 1,
  # 'photo': b'\x00\x01\x02\x03'
  # }

  try:
    game_schema_create.load(game)
  except ValidationError as err:
    print(err.messages)
    #TODO ask the user for input again
  return game

def get_next_turn(): 
  client = initialize_gpt_client()
  return

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



# messages=[
#       {"role": "system", "content": prompt},
#       {"role": "assistant", "content": '{ "description": "Welcome to the mysterious world of Aetheria. Aetheria is a land of magic, inhabited by creatures and beings of all kinds. Deep in the heart of the Enchanted Forest, you stand in awe as the sunlight filters through the towering trees. The air is filled with a soft, enchanting melody sung by unseen creatures. You can feel the magic in the air, tingling on your skin. The forest floor is covered in a thick carpet of moss and wild flowers, their vibrant colors creating a breathtaking sight. The scent of wild berries wafts to your nose, inviting you to explore further. Overhead, you can hear the gentle rustle of leaves as the wind whispers secrets to the trees. It\'s a place of wonder and danger, where adventure awaits at every turn.", "scene": "You stand at the edge of the Enchanted Forest, with tall trees stretching as far as the eye can see. Sunlight filters through the canopy, casting dappled shadows on the forest floor.", "health": "20/20", "weather": "The weather is warm and pleasant, with a gentle breeze ruffling your hair.", "location": "Enchanted Forest", "inventory": "None", "quests": "None", "possible_actions": "1. Explore deeper into the forest. 2. Look for a nearby town or village. 3. Set up camp and rest for the night." }'},
#       {"role": "user", "content": "Explore the world"}
#       ]