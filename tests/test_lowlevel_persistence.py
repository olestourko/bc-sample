import unittest

from src import app, db
from src.models import FeatureRequest, Client, ProductArea
import datetime

class TestLowlevelPersistence(unittest.TestCase):

    def setUp(self):
        app.config.from_object('tests.config')
        db.session.close()
        db.drop_all() # http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html
        db.create_all()
        db.session.add(Client(name="Client A"))
        db.session.add(Client(name="Client B"))
        db.session.add(ProductArea(name="Policies"))
        db.session.add(ProductArea(name="Billing"))
        self.feature = FeatureRequest(
            title="Test Feature",
            description="Dispose of the evidence",
            target_date=datetime.date.today() + datetime.timedelta(days=10)
        )

    def test_insert_delete_feature_request(self):
        db.session.add(self.feature)
        db.session.commit()
        found_feature = FeatureRequest.query.first()
        assert found_feature == self.feature
        found_feature.query.delete()
        found_feature = FeatureRequest.query.first()
        assert found_feature is None


    def test_associate_client_to_feature_request(self):
        db.session.add(self.feature)
        db.session.commit()
        client = Client.query.filter(Client.name == 'Client A').first()
        self.feature.clients.append(client)
        db.session.commit()
        found_feature = FeatureRequest.query.filter(FeatureRequest.title == 'Test Feature').first()
        assert found_feature == self.feature
        assert client in found_feature.clients

    def test_associate_product_area_to_feature_request(self):
        db.session.add(self.feature)
        db.session.commit()
        product_area = ProductArea.query.filter(ProductArea.name == 'Policies').first()
        self.feature.product_areas.append(product_area)
        db.session.commit()
        found_feature = FeatureRequest.query.filter(FeatureRequest.title == 'Test Feature').first()
        assert found_feature == self.feature
        assert product_area in found_feature.product_areas


if __name__ == '__main__':
    unittest.main()