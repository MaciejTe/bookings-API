import pytest
from flask_testing import TestCase

from src.database.models import db, Resources
from bookings_api import app
from tests import helpers


class TestResourcesEndpoint(TestCase):
    @classmethod
    def setup_class(cls):
        cls.url_root = 'http://127.0.0.1:5000/'
        with app.app_context():
            db.create_all()
            app.logger.info('Database initialized')
            helpers.insert_data_into_resources_table(Resources)

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_get_all_resources(self):
        """
        Test if all resources from resources_data.csv are correctly returned.
        """
        response = self.client.get('/resources')
        self.assertEqual(response.status_code, 200)
        exp_json = [
            {'active': True, 'created_at': '2018-10-10 10:10:10', 'id': 1, 'title': 'Sample Resource', 'updated_at': '2018-10-11 10:10:15'},
            {'active': False, 'created_at': '2018-10-10 05:05:05', 'id': 2, 'title': 'Johnny Bravo', 'updated_at': '2018-11-10 06:06:06'},
            {'active': False, 'created_at': '2017-01-03 07:07:07', 'id': 3, 'title': 'Adam Malysz', 'updated_at': '2017-02-02 11:12:13'}
        ]
        self.assertEqual(response.json, exp_json)

    @classmethod
    def teardown_class(cls):
        with app.app_context():
            db.drop_all()
            app.logger.info('Database dropped')
