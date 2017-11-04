from flask import render_template
from flask_migrate import Migrate
from src import app, db
from models import *

migrate = Migrate(app, db)

@app.route('/')
def render():
    return render_template('app.html')

def set_feature_client(feature, client):
    """
    Set the client for a feature request.
    Allow only one client per feature request.

    :param feature: FeatureRequest
    :param client: Client
    :return: feature
    """

    feature.clients = []
    feature.clients.append(client)
    return feature

def set_feature_product_area(feature, product_area):
    """
    Set the product area for a feature request.
    Allow only one product area per feature request.

    :param feature: FeatureRequest
    :param product_area: ProductArea
    :return: feature
    """

    feature.product_areas = []
    feature.product_areas.append(product_area)
    return feature

def set_feature_priority(feature, priority):
    """
    Set the client priority on a feature request.
    Client priority numbers should not repeat for the given client.

    :param feature:
    :param priority:
    :return: feature
    """

    feature.client_priority = priority
    return feature
