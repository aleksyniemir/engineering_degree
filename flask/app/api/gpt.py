import app.utils.gpt as gpt 
from flask import Blueprint, request, jsonify
from app.utils.auth import token_required
from app.schemas.game import game_schema_for_frontend
import app.utils.auth as auth
import app.crud.gpt as crud

from app import db

bp = Blueprint('gpt', __name__, url_prefix='/gpt')

@bp.route("/begin_game", methods = ['POST'])
@token_required
def begin_game():
    try:
        game_environment = request.json["game_environment"]
    except:
        return jsonify({"error": "No game environment specified"}), 400
    user = auth.get_current_user()
    game_data_schema = gpt.generate_game(user.id, game_environment)
    game = crud.add_game(db.session, game_data_schema)
    return game_schema_for_frontend.jsonify(game)

# @bp.route("/get_next_turn", methods = ['POST'])
# @token_required
# def get_next_turn(game_id)