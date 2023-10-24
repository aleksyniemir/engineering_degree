from marshmallow import fields
from flask_marshmallow import Marshmallow
from marshmallow import validate

ma = Marshmallow()

class UserSchemaBase(ma.Schema):
    id = fields.Int(dump_only=True)
    nick = fields.Str(required=True, validate=validate.Length(min=1), error_messages={"required": "Nickname is required"})
    email = fields.Str(required=True, error_messages={"required": "Email is required"})

class UserSchema(UserSchemaBase): ...

class UserSchemaPrivate(UserSchemaBase):
    password = fields.Str(required=True, validate=validate.Length(min=8), error_messages={"required": "Password is required"})

class UserSchemaCreate(UserSchemaBase):
    password = fields.Str(required=True, validate=validate.Length(min=8), error_messages={"required": "Password is required"})

class UserSchemaUpdate(ma.Schema):
    nick = fields.Str(validate=validate.Length(min=1))
    email = fields.Str() 
    password = fields.Str(validate=validate.Length(min=8))

class UserSchemaAuth(UserSchemaBase):
    token = ma.Str()

user_schema = UserSchema()
user_schema_create = UserSchemaCreate()
user_schema_private = UserSchemaPrivate()
user_schema_update = UserSchemaUpdate()  
user_schema_auth = UserSchemaAuth()  
users_schema = UserSchema(many=True)