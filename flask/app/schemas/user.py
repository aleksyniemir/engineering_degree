from flask import Flask, jsonify, request, make_response
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from marshmallow import fields, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from datetime import datetime, timedelta
from dotenv import load_dotenv
from functools import wraps
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class UserSchema(ma.Schema):
    nick = fields.Str()
    email = fields.Str()
    password = fields.Str()

user_schema = UserSchema()  
users_schema = UserSchema(many=True)