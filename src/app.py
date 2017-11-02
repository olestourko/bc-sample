
from flask_migrate import Migrate
from src import app, db
from models import *

migrate = Migrate(app, db)

@app.route('/')
def hello_world():
    return 'Got here'