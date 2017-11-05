import os, sys
sys.path.insert(0, os.getcwd()) # This makes the app, db import work
from sqlalchemy import exc
from src import app, db
from models import Client, ProductArea, FeatureRequest
import datetime
from src.application import set_feature_priority

def seed_db(database):
    try:
        client_1 = Client(name="Client A")
        product_area_1 = ProductArea(name="Policies")
        database.session.add(client_1)
        database.session.add(Client(name="Client B"))
        database.session.add(Client(name="Client C"))
        database.session.add(product_area_1)
        database.session.add(ProductArea(name="Billing"))
        database.session.add(ProductArea(name="Claims"))
        database.session.add(ProductArea(name="Reports"))

        feature_request = FeatureRequest(
            title="Feature Request 1",
            description="Suspendisse potenti. Nunc at lobortis velit, a condimentum leo. Donec pulvinar ac justo ac tristique.",
            target_date=datetime.date.today() + datetime.timedelta(days=100)
        )
        feature_request.clients.append(client_1)
        feature_request.product_areas.append(product_area_1)
        set_feature_priority(1)

        database.session.add(feature_request)

        database.session.commit()
    except exc.SQLAlchemyError:
        database.session.rollback()

if __name__ == "__main__":
    seed_db(db)