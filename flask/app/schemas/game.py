from marshmallow import fields, validate
from flask_marshmallow import Marshmallow   

ma = Marshmallow()

class GameSchemaBase(ma.Schema):
    id = fields.Int()
    photo = fields.Raw(required=True)
    description = fields.Str(required=True, validate=validate.Length(min=1, max=1023), error_messages={"required": "Description is required"})
    scene = fields.Str(required=True, validate=validate.Length(min=1, max=1023), error_messages={"required": "Scene is required"})
    turn_number = fields.Int(required=True)
    possible_actions = fields.Str(required=True, validate=validate.Length(min=1, max=1023), error_messages={"required": "Possible actions are required"})
    quests = fields.Str(required=True, validate=validate.Length(min=1, max=1023), error_messages={"required": "Quests are required"})
    inventory = fields.Str(required=True, validate=validate.Length(min=1, max=1023), error_messages={"required": "Inventory is required"})
    health = fields.Str(required=True, validate=validate.Length(min=1), error_messages={"required": "Health is required"})
    location = fields.Str(required=True, validate=validate.Length(min=1, max=1023), error_messages={"required": "Location is required"})
    weather = fields.Str(required=True, validate=validate.Length(min=1, max=1023), error_messages={"required": "Weather is required"})


class GameSchemaCreate(GameSchemaBase):
    user_id = fields.Int(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=1))
    prompt = fields.Str(required=True, validate=validate.Length(min=1, max=8191), error_messages={"required": "Prompt is required"})


class GameSchemaUpdate(ma.Schema):
    prompt = fields.Str()
    description = fields.Str()
    scene = fields.Str()
    turn_number = fields.Int()
    possible_actions = fields.Str()
    quests = fields.Str()
    inventory = fields.Str()
    health = fields.Str()
    location = fields.Str()
    weather = fields.Str()
    photo = fields.Raw()


class GameSchemaSimplified(ma.Schema):
    id = fields.Int()
    title = fields.Str()
    turn_number = fields.Int()

class GameSchemaForFrontend(GameSchemaBase):
    photo: fields.Str(required=True)
    

game_schema_create = GameSchemaCreate()
game_schema_update = GameSchemaUpdate()
game_schema_for_frontend = GameSchemaForFrontend()
game_schema_simplified = GameSchemaSimplified()
game_schemas_simplified = GameSchemaSimplified(many=True)