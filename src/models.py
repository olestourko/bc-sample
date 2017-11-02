from src import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

class FeatureRequest(db.Model):
    __tablename__ = 'feature_request'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    description = db.Column(db.Text())
    target_date = db.Column(db.Date())
    # Relation to Client
    feature_request_to_clients = relationship("FeatureRequestToClient", cascade="all, delete-orphan")
    feature_request_to_product_areas = relationship("FeatureRequestToProductArea", cascade="all, delete-orphan")
    clients = association_proxy("feature_request_to_clients", "client")
    product_areas = association_proxy("feature_request_to_product_areas", "product_area")

    @property
    def client_priority(self):
        if len(self.feature_request_to_clients) == 1:
            return self.feature_request_to_clients[0].client_priority
        else:
            return None

    @client_priority.setter
    def client_priority(self, value):
        if len(self.feature_request_to_clients) == 1:
            self.feature_request_to_clients[0].client_priority = value


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    # Relation to FeatureRequests



class ProductArea(db.Model):
    __tablename__ = 'product_area'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))


""" Flask Many-To-Many Relationships with extra fields:
    http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html?highlight=relationships#association-object
    Example: http://docs.sqlalchemy.org/en/latest/_modules/examples/association/proxied_association.html
"""
class FeatureRequestToClient(db.Model):
    __tablename__ = 'feature_request_to_client'
    feature_request_id = db.Column(db.Integer, db.ForeignKey('feature_request.id'), primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), primary_key=True)
    client_priority = db.Column(db.Integer)
    feature_request = db.relationship(FeatureRequest) # Can also do this with backrefs: http://docs.sqlalchemy.org/en/latest/orm/backref.html
    client = db.relationship(Client)

    def __init__(self, client, client_priority=None):
        self.client = client
        self.client_priority = client_priority


class FeatureRequestToProductArea(db.Model):
    __tablename__ = 'feature_request_to_product_area'
    feature_request_id = db.Column(db.Integer, db.ForeignKey('feature_request.id'), primary_key=True)
    product_area_id = db.Column(db.Integer, db.ForeignKey('product_area.id'), primary_key=True)
    feature_request = db.relationship(FeatureRequest)
    product_area = db.relationship(ProductArea)

    def __init__(self, product_area):
        self.product_area = product_area