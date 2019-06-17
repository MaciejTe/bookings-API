import pytest

from src.database.models import db, Slots
from bookings_api import app
from tests import helpers


class TestSlotsPositive:
    @classmethod
    def setup_class(cls):
        cls.url_root = "http://127.0.0.1:5000/"
        with app.app_context():
            db.create_all()
            app.logger.info("Database initialized")
            helpers.insert_test_data_into_db_table(Slots)

    @pytest.fixture(scope="module")
    def client(self):
        testing_client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        yield testing_client
        ctx.pop()

    def test_get_all_slots(self, client):
        """
        Test if all slots from slots_data.csv are correctly returned.
        """
        response = client.get("/slots")
        assert response.status_code == 200
        exp_json = [
            {
                "available_resources": "2",
                "formatted_timestamp": "Friday, March  8, 2018, 10:00 AM",
                "formatted_timestamp_end": "Friday, March  8, 2018, 10:15 AM",
                "free": 1,
                "id": 1,
                "maximum_capacity": 2,
                "timestamp": "2018-03-08 10:00:00",
                "timestamp_end": "2018-03-08 10:15:00",
            },
            {
                "available_resources": "1,2",
                "formatted_timestamp": "Friday, March  8, 2018, 10:00 AM",
                "formatted_timestamp_end": "Friday, March  8, 2018, 10:15 AM",
                "free": 2,
                "id": 2,
                "maximum_capacity": 2,
                "timestamp": "2018-03-08 10:00:00",
                "timestamp_end": "2018-03-08 10:15:00",
            },
            {
                "available_resources": "1,2",
                "formatted_timestamp": "Saturday, March  12, 2018, 13:00 AM",
                "formatted_timestamp_end": "Saturday, March  12, 2018, 14:00 AM",
                "free": 1,
                "id": 3,
                "maximum_capacity": 2,
                "timestamp": "2018-03-12 13:00:00",
                "timestamp_end": "2018-03-12 14:00:00",
            },
            {
                "available_resources": "3",
                "formatted_timestamp": "Tuesday, March  19, 2018, 13:00 AM",
                "formatted_timestamp_end": "Tuesday, March  19, 2018, 14:00 AM",
                "free": 1,
                "id": 4,
                "maximum_capacity": 3,
                "timestamp": "2018-03-19 13:00:00",
                "timestamp_end": "2018-03-19 14:00:00",
            },
            {
                "available_resources": "1,3",
                "formatted_timestamp": "Monday, April  4, 2018, 10:00 AM",
                "formatted_timestamp_end": "Monday, April  4, 2018, 10:15 AM",
                "free": 2,
                "id": 5,
                "maximum_capacity": 3,
                "timestamp": "2018-04-04 10:00:00",
                "timestamp_end": "2018-04-04 10:15:00",
            },
            {
                "available_resources": "1,2,3",
                "formatted_timestamp": "Thursday, May  6, 2018, 10:00 AM",
                "formatted_timestamp_end": "Thursday, May  6, 2018, 10:15 AM",
                "free": 3,
                "id": 6,
                "maximum_capacity": 4,
                "timestamp": "2018-05-06 10:00:00",
                "timestamp_end": "2018-05-06 10:15:00",
            },
        ]
        assert response.json == exp_json

    def test_get_slot_by_date(self, client):
        """ Get slot by its date. """
        response = client.get("/slots?from=2018-03-12")
        exp_json = [
            {
                "available_resources": "1,2",
                "formatted_timestamp": "Saturday, March  12, 2018, 13:00 AM",
                "formatted_timestamp_end": "Saturday, March  12, 2018, 14:00 AM",
                "free": 1,
                "id": 3,
                "maximum_capacity": 2,
                "timestamp": "2018-03-12 13:00:00",
                "timestamp_end": "2018-03-12 14:00:00",
            }
        ]
        assert response.status_code == 200
        assert response.json == exp_json

    def test_get_slot_by_date_range(self, client):
        """ Get list of slots filtered by date range. """
        response = client.get("/slots?from=2018-04-01&to=2018-06-01")
        exp_json = [
            {
                "available_resources": "1,3",
                "formatted_timestamp": "Monday, April  4, 2018, 10:00 AM",
                "formatted_timestamp_end": "Monday, April  4, 2018, 10:15 AM",
                "free": 2,
                "id": 5,
                "maximum_capacity": 3,
                "timestamp": "2018-04-04 10:00:00",
                "timestamp_end": "2018-04-04 10:15:00",
            },
            {
                "available_resources": "1,2,3",
                "formatted_timestamp": "Thursday, May  6, 2018, 10:00 AM",
                "formatted_timestamp_end": "Thursday, May  6, 2018, 10:15 AM",
                "free": 3,
                "id": 6,
                "maximum_capacity": 4,
                "timestamp": "2018-05-06 10:00:00",
                "timestamp_end": "2018-05-06 10:15:00",
            },
        ]
        assert response.status_code == 200
        assert response.json == exp_json

    def test_get_slot_by_resource(self, client):
        """ Get list of slots filtered by available resources. """
        response = client.get("/slots?resources=3")
        exp_json = [
            {
                "available_resources": "3",
                "formatted_timestamp": "Tuesday, March  19, 2018, 13:00 AM",
                "formatted_timestamp_end": "Tuesday, March  19, 2018, 14:00 AM",
                "free": 1,
                "id": 4,
                "maximum_capacity": 3,
                "timestamp": "2018-03-19 13:00:00",
                "timestamp_end": "2018-03-19 14:00:00",
            }
        ]
        assert response.status_code == 200
        assert response.json == exp_json

    @classmethod
    def teardown_class(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()
            app.logger.info("Database dropped")
