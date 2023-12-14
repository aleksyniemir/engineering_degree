import app.crud.gpt as crud 
from app.models.game import Game
from app import db
from app.utils.gpt import prompt

def test_add_game(client):
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
    user_id = 1
    game_id = 1
    title = 'Dune Adventure'
    photo = b'\x00\x01\x02\x03'

    created_game = crud.add_game(db.session, json, user_id, game_id, title, photo, prompt)

    game = crud.get_game_by_id(db.session, game_id)
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
