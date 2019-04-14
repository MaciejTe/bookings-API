import pytest

from src.database.models import db, Resources, Users, Bookings
from bookings_api import app
from tests import helpers


class TestBookingsPositive:
    @classmethod
    def setup_class(cls):
        cls.url_root = "http://127.0.0.1:5000/"
        with app.app_context():
            db.create_all()
            app.logger.info("Database initialized")
            helpers.insert_test_data_into_db_table(Resources)
            helpers.insert_test_data_into_db_table(Users)
            helpers.insert_test_data_into_db_table(Bookings)

    @pytest.fixture(scope="module")
    def client(self):
        testing_client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        yield testing_client
        ctx.pop()

    def test_get_all_bookings(self, client):
        """
        Test if all bookings from bookings_data.csv are correctly returned.
        """
        response = client.get("/bookings")
        assert response.status_code == 200
        exp_json = [
            {
                "booked_from": "Wed, 10 Apr 2019 10:00:00 GMT",
                "booked_to": "Wed, 10 Apr 2019 10:15:00 GMT",
                "id": 1,
                "notes": "sample note",
                "resource_id": 1,
                "user_id": 2,
            },
            {
                "booked_from": "Thu, 11 Apr 2019 12:30:00 GMT",
                "booked_to": "Thu, 11 Apr 2019 13:30:00 GMT",
                "id": 2,
                "notes": "",
                "resource_id": 2,
                "user_id": 1,
            },
            {
                "booked_from": "Sun, 14 Apr 2019 09:00:00 GMT",
                "booked_to": "Wed, 10 Apr 2019 10:00:00 GMT",
                "id": 3,
                "notes": "another note",
                "resource_id": 3,
                "user_id": 3,
            },
        ]
        assert response.json == exp_json

    def test_get_booking_by_id(self, client):
        """ Get booking by its ID. """
        response = client.get("/bookings?id=1")
        exp_json = [
            {
                "booked_from": "Wed, 10 Apr 2019 10:00:00 GMT",
                "booked_to": "Wed, 10 Apr 2019 10:15:00 GMT",
                "id": 1,
                "notes": "sample note",
                "resource_id": 1,
                "user_id": 2,
            }
        ]
        assert response.status_code == 200
        assert response.json == exp_json

    def test_get_booking_by_resource_id(self, client):
        """ Get booking by resource ID. """
        response = client.get("/bookings?resource-id=3")
        exp_json = [
            {
                "booked_from": "Sun, 14 Apr 2019 09:00:00 GMT",
                "booked_to": "Wed, 10 Apr 2019 10:00:00 GMT",
                "id": 3,
                "notes": "another note",
                "resource_id": 3,
                "user_id": 3,
            }
        ]
        assert response.status_code == 200
        assert response.json == exp_json

    def test_get_booking_by_user_id(self, client):
        """ Get booking by user ID. """
        response = client.get("/bookings?user-id=1")
        exp_json = [
            {
                "booked_from": "Thu, 11 Apr 2019 12:30:00 GMT",
                "booked_to": "Thu, 11 Apr 2019 13:30:00 GMT",
                "id": 2,
                "notes": "",
                "resource_id": 2,
                "user_id": 1,
            }
        ]
        assert response.status_code == 200
        assert response.json == exp_json

    def test_add_booking(self, client):
        """ Add booking to database. """
        post_response = client.post(
            "/bookings",
            json=dict(
                resource_id=2,
                user_id=1,
                booked_from="2019-04-18 13:00:00",
                booked_to="2019-04-18 14:00:00",
                notes="test note",
            ),
        )
        assert post_response.status_code == 200
        assert post_response.json["success"] is True
        get_response = client.get("/bookings?id=4")
        assert get_response.json[0]["resource_id"] == 2
        assert get_response.json[0]["user_id"] == 1
        assert get_response.json[0]["booked_from"] == "Thu, 18 Apr 2019 13:00:00 GMT"
        assert get_response.json[0]["booked_to"] == "Thu, 18 Apr 2019 14:00:00 GMT"
        assert get_response.json[0]["id"] == 4

    def test_update_booking_resource_id(self, client):
        """ Update existing booking. """
        put_response = client.put("/bookings", json=dict(id=4, resource_id=3))
        assert put_response.status_code == 200
        get_response = client.get("/bookings?id=4")
        assert get_response.json[0]["resource_id"] == 3

    def test_update_booking_booked_from_to(self, client):
        """ Update existing booking. """
        put_response = client.put(
            "/bookings",
            json=dict(
                id=4, booked_from="2019-04-19 13:00:00", booked_to="2019-04-19 14:00:00"
            ),
        )
        assert put_response.status_code == 200
        get_response = client.get("/bookings?id=4")
        assert get_response.json[0]["resource_id"] == 3
        assert get_response.json[0]["booked_from"] == "Fri, 19 Apr 2019 13:00:00 GMT"
        assert get_response.json[0]["booked_to"] == "Fri, 19 Apr 2019 14:00:00 GMT"

    def test_delete_booking(self, client):
        """ Delete existing booking using its ID. """
        delete_response = client.delete("/bookings?id=4")
        assert delete_response.status_code == 200
        assert delete_response.json["success"] is True
        get_response = client.get("/resources?id=4")
        assert get_response.json == []
        assert get_response.status_code == 200

    @classmethod
    def teardown_class(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()
            app.logger.info("Database dropped")
