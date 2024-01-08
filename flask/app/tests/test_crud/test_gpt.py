import app.crud.gpt as crud 
from app.models.game import Game
from app.schemas.game import game_schema_create
from app import db

def test_add_game(client):
    game_dict = {
        'description': 'You are a brave adventurer who has arrived on the desert planet of Arrakis, also known as Dune. The planet is known for its harsh and inhospitable conditions, with towering sand dunes and scorching heat. You have come to this unforgiving world in search of the valuable resource known as spice, which is found only on Arrakis. Spice is highly sought after and can be used for a variety of purposes, including interstellar travel and extending life. As you step out of your ship and onto the sandy surface of Dune, you take a moment to absorb the vastness of the desert before you.',
        'scene': 'The sun beats down relentlessly, casting long shadows across the shifting sand dunes. The wind howls, carrying with it the sound of sand grains swirling and scraping against each other.',
        'health': '20/20',
        'weather': 'Hot and dry',
        'location': 'Arrakis (Dune)',
        'inventory': 'Empty',
        'quests': 'None',
        'possible_actions': 'Explore the surroundings, look for a settlement, search for water',
        'user_id': 1, 
        'prompt': "test",
        'title':'Dune Adventure',
        'photo': b'\x00\x01\x02\x03'
    }

    game_data = game_schema_create.load(game)
    created_game = crud.add_game(db.session, game_data)

    game = crud.get_game_by_id(db.session, created_game.id)
    assert isinstance(game, Game)
    assert game.id == created_game.id
    assert game.title == created_game.title
    assert game.photo == created_game.photo
    assert game.prompt == created_game.prompt

def test_update_game():
    json = {
        'Description': 'You are a brave adventurer who has arrived on the desert planet of Arrakis, also known as Dune. The planet is known for its harsh and inhospitable conditions, with towering sand dunes and scorching heat. You have come to this unforgiving world in search of the valuable resource known as spice, which is found only on Arrakis. Spice is highly sought after and can be used for a variety of purposes, including interstellar travel and extending life. As you step out of your ship and onto the sandy surface of Dune, you take a moment to absorb the vastness of the desert before you.',
        'Scene': 'The sun beats down relentlessly, casting long shadows across the shifting sand dunes. The wind howls, carrying with it the sound of sand grains swirling and scraping against each other.',
        'Health': '20/20',
        'Weather': 'Hot and dry',
        'Location': 'Arrakis (Dune)',
        'Inventory': 'Empty',
        'Quests': 'None',
        'Possible actions': 'Explore the surroundings, look for a settlement, search for water'
    }
    game_id = 1
    turn_number = 2
    photo = b'\x00\x01\x02\x03'
    prompt = 'What will you do next?'

    created_game = crud.update_game(db.session, json, game_id, turn_number, photo, prompt)

    game = crud.get_game_by_id(db.session, game_id)
    assert isinstance(game, Game)
    assert game.id == created_game.id
    assert game.title == created_game.title
    assert game.photo == created_game.photo
    assert game.prompt == created_game.prompt



def test_remove_game(client):
    game_dict = {
        'description': 'You are a brave adventurer...',
        'scene': 'The sun beats down relentlessly...',
        'health': '20/20',
        'weather': 'Hot and dry',
        'location': 'Arrakis (Dune)',
        'inventory': 'Empty',
        'quests': 'None',
        'possible_actions': 'Explore the surroundings, look for a settlement, search for water',
        'user_id': 1, 
        'prompt': "test",
        'title':'Dune Adventure',
        'photo': b'\x00\x01\x02\x03',
        'turn_number': 1
    }
    game_data = game_schema_create.load(game_dict)
    created_game = crud.add_game(db.session, game_data)

    game_id = created_game.id

    crud.remove_game(db.session, game_id)

    game = crud.get_game_by_id(db.session, game_id)
    assert game is None

