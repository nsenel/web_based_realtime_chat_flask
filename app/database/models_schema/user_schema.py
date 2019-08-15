# src/database/schema/user_schema.py

from marshmallow import Schema, fields, pre_dump
class UserSchema(Schema):
        # Fields to expose
        ordered      = True
        user_id      = fields.Int()
        user_name    = fields.Str()