from marshmallow import Schema, fields


class CustomerSchema(Schema):
    id = fields.Integer(required=True)
    username = fields.String(required=True)
