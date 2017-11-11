## BC Flask Sample
This is a sample web application built with Python.

---

#### Dependencies


##### [Flask](http://flask.pocoo.org/docs/0.12/quickstart/)
The web application framework.

```
pip install flask
```

##### [SQLAlchemy](https://www.sqlalchemy.org/)
The ORM (+ some extensions).

```
pip install mysql-python #<- Will probably require _libmysqlclient_ (sudo apt-get install libmysqlclient-dev)
pip install sqlalchemy
pip install flask-sqlalchemy
pip install flask-migrate
```

- [Flask Integration](http://flask.pocoo.org/docs/0.12/quickstart/)
- [Migrations Extension](https://flask-migrate.readthedocs.io/en/latest/)

##### [Marshmallow](https://marshmallow.readthedocs.io/en/latest/)
Model mapper for SQLAlchemy model -> JSON.

```
pip install marshmallow
```

---

#### Running It

First get the dependencies above, then...

**Initial Migrations and Seeding**

First specifiy your database credentials in a file called `/config.py`. (check out /`example_config.py`)

```
flask migrate init
flask db migrate
flask db upgrade
```

Seed the db with clients and product ares:

```
python src/seed.py
```

**Get frontend packages**

Requires [yarnpkg](https://yarnpkg.com/lang/en/docs/install/):
```
yarn install
```

**Start the Flask server**

From the `bc-sample` directory:
```
FLASK_APP=$(pwd)/src/application.py
CONFIG_FILEPATH=$(pwd)/config.py
export FLASK_APP
export CONFIG_FILEPATH
flask run
```
Note: You should use a proper application server like uWSGI in production, but this is good enough for demo purposes.

---

#### Unit tests
They're in the `/tests` folder. Similair to running the application, set an env variable with the config file location. You should set up a seperate DB just for tests.
```
CONFIG_FILEPATH=$(pwd)/tests/config.py
export CONFIG_FILEPATH
python -m unittest discover
```

---

### Q&A / Implementation Notes:
**What was the general development workflow?**

1. Set up DB tables and ORM linkage
2. Create persistence service and its unit tests
3. Create web endpoints, including input validation
4. Create page templates and all the frontend fluff

**Why are you using _many-to-many_ relationships with an associative object when you can just use simple _one-to-one_ and _one-to-many relationships_ instead?**

1. Future extensibility. What if a feature request can have multiple product areas or involve multiple clients? This has come up a lot in my experience.
2. It lets me embed extra information about a relation into its own table, for example `client_priority`.

**How/why did you handle the Client Priority constraint?**

I chose to check if a FeatureRequest / Client pair already existed with the selected priority, and block creation if so. The other option would have been to automatically rearrange all the other priorities to accommodate the new one, but chose not to since this would probably be more confusing for the end user.

**Features that could be added:**

1. _Edit_ form for existing feature requests.
2. _Search_ and _Sort_ tools for narrowing down existing feature requests.
3. Prettier UI: datepicker, fancy styles.