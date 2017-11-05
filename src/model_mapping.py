from models import *
from marshmallow import Schema, fields

class ClientSchema(Schema):
    id = fields.Integer()
    name = fields.Str()

class ProductAreaSchema(Schema):
    id = fields.Integer()
    name = fields.Str()

class FeatureRequestSchema(Schema):
    id = fields.Integer()
    title = fields.Str()
    description = fields.Str()
    target_date = fields.Date()
    clients = fields.Nested(ClientSchema, many=True)
    product_areas = fields.Nested(ProductAreaSchema, many=True)
    # http://marshmallow.readthedocs.io/en/latest/custom_fields.html#function-fields
    priority = fields.Function(lambda obj: obj.feature_request_to_clients[0].client_priority)
