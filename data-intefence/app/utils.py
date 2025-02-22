from marshmallow import Schema, fields

class TransDetailSchema(Schema):
    user_id = fields.Int(required=True)

class TransSumSchema(Schema):
    user_ids = fields.List(fields.Int(), required=False)