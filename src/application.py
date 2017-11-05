from flask import render_template, request, jsonify
from flask_migrate import Migrate
from src import app, db
from models import *
from model_mapping import ClientSchema, ProductAreaSchema, FeatureRequestSchema

migrate = Migrate(app, db)

@app.route('/')
def render():
    return render_template('app.html')

@app.route('/fetch_clients')
def fetch_clients():
    clients = Client.query.all()
    schema = ClientSchema()
    result = [schema.dump(client).data for client in clients]
    return jsonify(result)

@app.route('/fetch_product_areas')
def fetch_product_areas():
    product_areas = ProductArea.query.all()
    schema = ProductAreaSchema()
    result = [schema.dump(product_area).data for product_area in product_areas]
    return jsonify(result)

@app.route('/fetch_feature_requests')
def fetch_feature_requests():
    feature_requests = FeatureRequest.query.all()
    schema = FeatureRequestSchema()
    result = [schema.dump(feature_request).data for feature_request in feature_requests]
    return jsonify(result)

@app.route('/create_feature_request', methods=['POST'])
def create_feature_request():
    from datetime import datetime
    date = datetime.strptime(request.form['targetDate'], '%d-%m-%Y').date()
    feature_request = FeatureRequest(
        title=request.form['title'],
        description=request.form['description'],
        target_date=datetime.strptime(request.form['targetDate'], '%d-%m-%Y').date()
    )

    client = Client.query.get(request.form['clientId'])
    product_area = ProductArea.query.get(request.form['productAreaId'])
    set_feature_client(feature_request, client)
    set_feature_product_area(feature_request, product_area)
    set_feature_priority(feature_request, request.form['priority'])

    # db.session.add(feature_request)
    # db.session.commit()
    return jsonify({
        'status': 'ok'
    })

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
