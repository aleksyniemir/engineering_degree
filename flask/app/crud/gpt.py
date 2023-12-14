from app.models.game import Game
from sqlalchemy import select

from app import db

def get_game_by_id(session: db.session, id: int):
    stmt = select(Game).where(Game.id==id)
    game = session.scalar(stmt)
    return game

def add_game(
        session: db.session,
        json: dict, 
        user_id: int, 
        game_id: int, 
        title: str, 
        photo: bytes,
        prompt: str):
    game = Game(
        id=game_id,
        user_id=user_id,
        title=title,
        photo=photo,
        prompt=prompt,
        description=json["Description"],
        scene=json["Scene"],
        turn_number=1,
        possible_actions=json["Possible actions"],
        quests=json["Quests"],
        inventory=json["Inventory"],
        health=json["Health"],
        location=json["Location"],
        weather=json["Weather"],
    )
    session.add(game)
    session.commit()
    return game

def update_game(
        session: db.session,
        json: dict, 
        game_id: int,
        turn_number: int, 
        photo: bytes,
        prompt: str):
    game = get_game_by_id(session, game_id)
    if game is None:
        return None

    game.photo = photo
    game.prompt = prompt
    game.description = json["Description"]
    game.scene = json["Scene"]
    game.turn_number = turn_number,
    game.possible_actions = json["Possible actions"]
    game.quests = json["Quests"]
    game.inventory = json["Inventory"]
    game.health = json["Health"]
    game.location = json["Location"]
    game.weather = json["Weather"]

    session.add(game)
    session.commit()
    return game

