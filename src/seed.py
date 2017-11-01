from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from app import Client, ProductArea


def seed_db(database):
    try:
        database.session.add(Client(name="Client A"))
        database.session.add(Client(name="Client B"))
        database.session.add(Client(name="Client C"))
        database.session.add(ProductArea(name="Policies"))
        database.session.add(ProductArea(name="Billing"))
        database.session.add(ProductArea(name="Claims"))
        database.session.add(ProductArea(name="Reports"))
        database.session.commit()
    except exc.SQLAlchemyError:
        database.session.rollback()

if __name__ == "__main__":
    app = Flask(__name__)
    app.config.from_envvar('CONFIG_FILEPATH')  # http://flask.pocoo.org/docs/0.12/config/
    db = SQLAlchemy(app)
    seed_db(db)