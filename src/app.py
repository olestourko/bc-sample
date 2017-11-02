
from flask_migrate import Migrate
from src import app, db

migrate = Migrate(app, db)

class FeatureRequest(db.Model):
    __tablename__ = 'feature_request'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    description = db.Column(db.Text())
    target_date = db.Column(db.Date())
    # Relation to Client
    # Relation to ProductArea
    pass


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    # Relation to FeatureRequests
    pass


class ProductArea(db.Model):
    __tablename__ = 'product_area'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    pass


""" Flask Many-To-Many Relationships with extra fields:
    http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html?highlight=relationships#association-object 
"""
""" Add some intermediary table for Client -> FeatureRequest Mappings
    id
    feature_request_id
    client_id
    client_priority: Client Priority numbers should not repeat for the given client
"""
class FeatureRequestToClient(db.Model):
    __tablename__ = 'feature_request_to_client'
    feature_request_id = db.Column(db.Integer, db.ForeignKey('feature_request.id'), primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), primary_key=True)
    client_priority = db.Column(db.Integer)
    feature_request = db.relationship("FeatureRequest")

""" Add some intermediary table for FeatureRequest -> ProductArea Mappings
    id
    feature_request_id
    product_area_id
"""


class FeatureRequestToProductArea(db.Model):
    __tablename__ = 'feature_request_to_product_area'
    feature_request_id = db.Column(db.Integer, db.ForeignKey('feature_request.id'), primary_key=True)
    product_area_id = db.Column(db.Integer, db.ForeignKey('product_area.id'), primary_key=True)
    product_area = db.relationship("ProductArea")


@app.route('/')
def hello_world():
    return 'Got here'