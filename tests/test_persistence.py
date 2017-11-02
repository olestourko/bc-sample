import unittest

from src import app, db
from src.app import FeatureRequest
import datetime

class TestPersistence(unittest.TestCase):

    def setUp(self):
        app.config.from_object('tests.config')
        db.session.close()
        db.drop_all() # http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html
        db.create_all()

    def test_insert_feature_request(self):
        feature = FeatureRequest(
            title="Test Feature",
            description="Dispose of the evidence",
            target_date=datetime.date.today() + datetime.timedelta(days=10)
        )
        db.session.add(feature)
        db.session.commit()
        found_feature = FeatureRequest.query.first()
        assert found_feature.title == feature.title
        assert found_feature.description == feature.description
        assert found_feature.target_date == feature.target_date

    def test_delete_feature_request(self):
        pass

    def test_associate_feature_request(self):
        pass

    def test_set_priority(self):
        pass

if __name__ == '__main__':
    unittest.main()