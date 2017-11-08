## BC Flask Sample
This is a sample web application built with Python.

1. Set up DB tables and ORM linkage
2. Create persistence service and its unit tests
3. Create web endpoints, including input validation
4. Create page templates and all the frontend fluff

---

#### [Flask](http://flask.pocoo.org/docs/0.12/quickstart/)
The web application framework.

`pip install flask`

#### [SQLAlchemy](https://www.sqlalchemy.org/)
The ORM (+ some extensions).


`pip install mysql-python` <- Will probably require _libmysqlclient_ (`sudo apt-get install libmysqlclient-dev`)
`pip install sqlalchemy`
`pip install flask-sqlalchemy`
`pip install flask-migrate`

- [Flask Integration](http://flask.pocoo.org/docs/0.12/quickstart/)
- [Migrations Extension](https://flask-migrate.readthedocs.io/en/latest/)

#### [Marshmallow](https://marshmallow.readthedocs.io/en/latest/)

`pip install marshmallow`

Model mapper for SQLAlchemy model -> JSON.

---

#### Running It

Initial migrations:
```
flask migrate init
flask db migrate
flask db upgrade
```

Running the application (from the `bc-sample` directory):
```
FLASK_APP = $(pwd)/src/application.py
CONFIG_FILEPATH = $(pwd)/config.py
export FLASK_APP
export CONFIG_FILEPATH
flask run
```

---

### Q&A
**Q:**
Why are you using _many-to-many_ relationships with an associative object when you can just use simple _one-to-one_ and _one-to-many relationships_ instead?

**A:**
1. Future extensibility. What if a feature request can have multiple product areas or involve multiple clients? This has come up a lot in my experience.
2. It lets me embed extra information about a relation into its own table, for example `client_priority`.