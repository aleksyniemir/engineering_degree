import app.utils.gpt as gpt
from app.models.game import Game
from sqlalchemy import select

from app.schemas.game import   game_schema_create, GameSchemaCreate
from app import db
from app.models.game import Game
from sqlalchemy import delete

def get_game_by_id(session: db.session, id: int):
    stmt = select(Game).where(Game.id==id)
    game = session.scalar(stmt)
    return game

def get_listed_games(session: db.session, user_id: int):
    stmt = select(Game).where(Game.user_id==user_id)
    games = session.scalars(stmt).all()
    return games

def add_game(session, game_data):
    # game_schema = game_schema_create.load(game_dict)
    game = Game(
        user_id=game_data["user_id"],
        title=game_data["title"],
        photo=game_data["photo"],
        prompt=game_data["prompt"],
        description=game_data["description"],
        scene=game_data["scene"],
        turn_number=game_data["turn_number"],
        possible_actions=game_data["possible_actions"],
        quests=game_data["quests"],
        inventory=game_data["inventory"],
        health=game_data["health"],
        location=game_data["location"],
        weather=game_data["weather"]
        )
    session.add(game)
    session.commit()
    return game

def update_game(
        session: db.session,
        game_id: int,
        command: str):
    game = get_game_by_id(session, game_id)

    if game is None:
        return None
    
    game_data = gpt.get_next_turn(game, command)
    game = Game(**game_data)
    session.add(game)
    session.commit()
    return game


def remove_game(session: db.session, game_id: int):
    game = get_game_by_id(session, game_id)

    if game is None:
        return None
    
    stmt = delete(Game).where(Game.id == game_id)
    session.execute(stmt)
    session.commit()
    return game

