import unittest

from src import app, db
from src.models import FeatureRequest, Client, ProductArea
import datetime
from src.application import set_feature_client, set_feature_product_area, set_feature_priority


class TestHighlevelPersistence(unittest.TestCase):

    def setUp(self):
        app.config.from_object('tests.config')
        db.session.close()
        db.drop_all() # http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html
        db.create_all()
        db.session.add(FeatureRequest(
            title="Test Feature",
            description="Dispose of the evidence",
            target_date=datetime.date.today() + datetime.timedelta(days=10)
        ))
        db.session.add(Client(name="Client A"))
        db.session.add(Client(name="Client B"))
        db.session.add(ProductArea(name="Policies"))
        db.session.add(ProductArea(name="Billing"))

    def test_set_feature_client(self):
        feature = FeatureRequest.query.filter(FeatureRequest.title == "Test Feature").first()
        client_a = Client.query.filter(Client.name == "Client A").first()
        client_b = Client.query.filter(Client.name == "Client B").first()

        """ Test setting a client on a feature request with no clients already set """
        set_feature_client(feature, client_a)
        db.session.commit()
        feature = FeatureRequest.query.filter(FeatureRequest.title == "Test Feature").first()
        assert client_a in feature.clients

        """ Test setting a client on a feature request which already has a client set """
        set_feature_client(feature, client_b)
        db.session.commit()
        feature = FeatureRequest.query.filter(FeatureRequest.title == "Test Feature").first()
        assert client_a not in feature.clients
        assert client_b in feature.clients

    def test_set_feature_product_area(self):
        feature = FeatureRequest.query.filter(FeatureRequest.title == "Test Feature").first()
        product_area_a = ProductArea.query.filter(ProductArea.name == "Policies").first()
        product_area_b = ProductArea.query.filter(ProductArea.name == "Billing").first()

        """ Test setting a client on a feature request with no clients already set """
        set_feature_product_area(feature, product_area_a)
        db.session.commit()
        feature = FeatureRequest.query.filter(FeatureRequest.title == "Test Feature").first()
        assert product_area_a in feature.product_areas

        """ Test setting a client on a feature request which already has a client set """
        set_feature_product_area(feature, product_area_b)
        db.session.commit()
        feature = FeatureRequest.query.filter(FeatureRequest.title == "Test Feature").first()
        assert product_area_a not in feature.product_areas
        assert product_area_b in feature.product_areas

    def test_set_feature_priority(self):
        feature = FeatureRequest.query.filter(FeatureRequest.title == "Test Feature").first()
        client_a = Client.query.filter(Client.name == "Client A").first()
        set_feature_client(feature, client_a)
        set_feature_priority(feature, 10)
        db.session.commit()
        feature = FeatureRequest.query.filter(FeatureRequest.title == "Test Feature").first()
        assert feature.client_priority == 10


if __name__ == '__main__':
    unittest.main()