from sqlalchemy import select, delete
from sqlalchemy.orm import Session

import app.utils.gpt as gpt
from app.models.game import Game


def get_game_by_id(session: Session, id: int):
    stmt = select(Game).where(Game.id==id)
    game = session.scalar(stmt)
    return game

def get_listed_games(session: Session, user_id: int):
    stmt = select(Game).where(Game.user_id==user_id)
    games = session.scalars(stmt).all()
    return games

def add_game(session: Session, game_data: dict):
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

def update_game(session: Session, game_id: int, command: str):
    game = get_game_by_id(session, game_id)

    if game is None:
        return None
    
    game_data = gpt.get_next_turn(game.prompt, command, game.turn_number)
    for key, value in game_data.items():
        setattr(game, key, value)
    session.commit()
    return game

def remove_game(session: Session, game_id: int):
    game = get_game_by_id(session, game_id)

    if game is None:
        return None
    
    stmt = delete(Game).where(Game.id == game_id)
    session.execute(stmt)
    session.commit()
    return game

