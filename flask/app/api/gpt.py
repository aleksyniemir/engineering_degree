import app.utils.gpt as gpt 
from flask import Blueprint, request, jsonify
from app.utils.auth import token_required
from app.schemas.game import *
import app.utils.auth as auth
import app.crud.gpt as crud
import base64

from app import db

bp = Blueprint('gpt', __name__, url_prefix='/gpt')


@bp.route("/get_game/<game_id>", methods = ["GET"])
@token_required
def get_game(game_id: int):
    user = auth.get_current_user()
    game = crud.get_game_by_id(db.session, game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    if game.user_id != user.id:
        return jsonify({"error": "You do not have enough permissions"}), 401
    game.photo = base64.b64encode(game.photo).decode('utf-8')
    return game_schema_for_frontend.jsonify(game)

@bp.route("/listed_games", methods = ['GET'])
@token_required
def listed_games():
    user = auth.get_current_user()
    games = crud.get_listed_games(db.session, user.id)
    return game_schemas_simplified.jsonify(games)

@bp.route("/begin_game", methods = ['POST'])
@token_required
def begin_game():
    try:
        game_environment = request.json["game_environment"]
    except:
        return jsonify({"error": "No game environment specified"}), 400
    user = auth.get_current_user()
    game_data = gpt.generate_game(user.id, game_environment)
    game = crud.add_game(db.session, game_data)
    game.photo = base64.b64encode(game.photo).decode('utf-8')
    return game_schema_for_frontend.jsonify(game)

@bp.route("/get_next_turn/<game_id>", methods = ['POST'])
@token_required
def get_next_turn(game_id: int):
    try:
        command = request.json["input"]
    except: 
        return jsonify({"error": "No input specified"}), 400
    user = auth.get_current_user()
    game = crud.get_game_by_id(db.session, game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    if game.user_id != user.id:
        return jsonify({"error": "You do not have enough permissions"}), 401
    
    game = crud.update_game(db.session, game_id, command)
    game.photo = base64.b64encode(game.photo).decode('utf-8')
    return game_schema_for_frontend.jsonify(game)


@bp.route("/remove_game/<game_id>", methods=['DELETE'])
@token_required
def remove_game(game_id: int):
    user = auth.get_current_user()
    game = crud.get_game_by_id(db.session, game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    if game.user_id != user.id:
        return jsonify({"error": "You do not have enough permissions"}), 401
    
    crud.remove_game(db.session, game_id)
    return jsonify({'message': 'Game removed successfully'})
