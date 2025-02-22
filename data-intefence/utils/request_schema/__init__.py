from marshmallow import Schema, fields

class TransDetailSchema(Schema):
    request_id = fields.Str(required=True)
    queries = fields.Str(required=True)
    model_name = fields.Str(missing="gpt-4o")

class TransSumSchema(Schema):
    request_id = fields.Str(required=True)
    queries = fields.Str(required=True)
    model_name = fields.Str(missing="gpt-4o")