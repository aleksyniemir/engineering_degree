from marshmallow import fields
from flask_marshmallow import Marshmallow   

ma = Marshmallow()

class GameSchemaBase(ma.Schema):
    game_id: int
    photo: bytes
    prompt: str
    description: str
    scene: str
    turn_number: int
    possible_actions: str
    quests: str
    inventory: str
    health: int
    locataion: str
    weather: str

class GameSchemaUpdate(GameSchemaBase):
    ...

class GameSchemaCreate(GameSchemaBase):
    user_id: int
    title: str

class GameSchemaForFrontend(GameSchemaBase):
    ...

game_create_schema = GameSchemaCreate()
game_update_schema = GameSchemaUpdate()
game_schema_for_frontend = GameSchemaForFrontend()