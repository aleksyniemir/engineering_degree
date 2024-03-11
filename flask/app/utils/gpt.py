import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from marshmallow import ValidationError

from app.utils.stable_diffusion import get_image
from app.schemas.game import game_schema_create, game_schema_update

load_dotenv()

def initialize_gpt_client():
  client = OpenAI(
      organization="org-M3Ibgl6TbM8lwc9aKuANBNsz",
      api_key = os.getenv("OPENAI_API_KEY")
  ) 
  return client

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
  4. 'description' must stay between 5 to 10 sentences. Change it every round. Remember about game environment: {game_environment}. You are a game master, so create an appropriate description. In every turn add unexpected events, new characters, or something that will make the game interesting.
  5. 'scene' is a prompt for a text-to-image model. It must describe what the player sees based on description. Change it every round.
  6. 'health' is a number from 0 to 20. The player starts with 20. If it reaches 0 or below, the player dies and the game is over (He can start the game again. Game must write completly different story). The player can lose all of his health and die by doing risky stuff. The player can gain health by eating, drinking, or sleeping. 
  7. 'weather' is dependent on the description. It must stay between 1 to 3 words. 
  8. 'location' is just a name of the place where the player is. It must stay between 1 to 3 words.  
  9. 'inventory' is a list of items that the player has. The player can gain items by picking them up or by buying them. The player can lose items by dropping them or by selling them. The player can use items by eating them, drinking them, or by using them. The player can only use items that he has in his inventory. If empty, write 'None'.
  10. 'quests' can be created by the game or can be gained from talking to people. If empty, write 'None'. Player can have only one quest. 'quests' must be up to 25 characters long.
  11. 'possible_actions' are representing what the player can do next. Every action should be very short. There should be three possible actions. Example: "['Kill the intruder', 'Talk to intruder', 'Escape through the window']". It must be a string. Use double quotes outside, and single quotes inside the list. The string should begin with "['. Then between the actions there should be ', '. And at the end there should be ']"  

  Start the game.
  '''
  data = {"role": "system", "content":prompt}
  messages = [data]
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
  )

  print(completion.choices[0].message.content)
  game = json.loads(completion.choices[0].message.content)

  response = {"role": "assistant", "content": f"""{completion.choices[0].message.content}"""}
  messages.append(response)  
  game["user_id"] = user_id
  game["title"] = game_environment
  game["prompt"] = json.dumps(messages)
  game["turn_number"] = 1
  game['photo'] = get_image(prompt=game['scene'])

  # MOCK DATA 
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
  # 'photo': get_image(prompt="Forest with a waterfall")
  # }

  try:
    game_schema_create.load(game)
  except ValidationError as err:
    print(err.messages)
  return game

def get_next_turn(prompt: str, command: str, turn_number: int): 
  client = initialize_gpt_client()
  messages = json.loads(prompt)
  messages.append({"role": "user", "content": f"""{command}"""})
  if len(messages) > 7:
    del messages[1:3]
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
  )
  response = {"role": "assistant", "content": f"""{completion.choices[0].message.content}"""}
  print(completion.choices[0].message.content)
  messages.append(response)  
  game = {}
  game["prompt"] = json.dumps(messages)
  game["scene"] = json.loads(completion.choices[0].message.content)["scene"]
  game['photo'] = get_image(prompt=game['scene'])
  game["turn_number"] = turn_number + 1
  game["description"] = json.loads(completion.choices[0].message.content)["description"]
  game["health"] = json.loads(completion.choices[0].message.content)["health"]
  game["weather"] = json.loads(completion.choices[0].message.content)["weather"]
  game["location"] = json.loads(completion.choices[0].message.content)["location"]
  game["inventory"] = json.loads(completion.choices[0].message.content)["inventory"]
  game["quests"] = json.loads(completion.choices[0].message.content)["quests"]
  game["possible_actions"] = json.loads(completion.choices[0].message.content)["possible_actions"]
  try:
    game_schema_update.load(game)
  except ValidationError as err:
    print(err.messages)
  return game
