import pytest

from src.database.models import db, Bookings
from bookings_api import app
from tests import helpers


class TestBookingsNegative:
    @classmethod
    def setup_class(cls):
        cls.url_root = "http://127.0.0.1:5000/"
        with app.app_context():
            db.create_all()
            app.logger.info("Database initialized")
            helpers.insert_test_data_into_db_table(Bookings)

    @pytest.fixture(scope="module")
    def client(self):
        testing_client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        yield testing_client
        ctx.pop()

    def test_get_non_existent_booking_by_id(self, client):
        """ Provide non existent booking ID to search for. """
        response = client.get("/bookings?id=123")
        assert response.json == []
        assert response.status_code == 200

    def test_get_non_existent_booking_by_resource_id(self, client):
        """ Search for non existent booking by resource ID. """
        response = client.get("/bookings?resource-id=43")
        assert response.json == []
        assert response.status_code == 200

    def test_get_non_existent_booking_by_user_id_and_id(self, client):
        """ Search for non existent booking by user ID title and booking id. """
        response = client.get("/bookings?user-id=67&id=123")
        assert response.json == []
        assert response.status_code == 200

    def test_get_booking_with_json(self, client):
        """ Try to filter GET results with JSON body. """
        response = client.get("/bookings", json=dict(id=1))
        assert response.status_code == 406
        assert response.json["errors"] == "JSON body is not accepted in this endpoint"
        assert response.json["success"] is False

    def test_get_booking_with_improper_filter(self, client):
        """ Use improper filter in GET /bookings. """
        response = client.get("/bookings?asd=123s")
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
        assert response.status_code == 200
        assert response.json == exp_json

    def test_improper_key_when_adding_booking(self, client):
        """ Use improper JSON key in POST request. """
        post_response = client.post("/bookings", json=dict(asd="Janusz"))
        assert post_response.status_code == 406
        assert post_response.json["success"] is False
        assert post_response.json["message"] == "Invalid input"
        assert post_response.json["errors"] == [
            "'resource_id' is a required property",
            "'user_id' is a required property",
            "'booked_from' is a required property",
            "'booked_to' is a required property",
        ]

    def test_update_non_existent_booking(self, client):
        """ Update non existent booking. """
        booking_id = 671
        put_response = client.put(
            "/bookings", json=dict(id=booking_id, booked_from="improper date")
        )
        assert put_response.status_code == 404
        assert put_response.json["message"] == "Booking not found"
        assert put_response.json["success"] is False
        assert (
            put_response.json["errors"]
            == f"Booking with given ID: {booking_id} was not found"
        )

    def test_update_without_params(self, client):
        """ Try to update booking without parameters to update. """
        res_id = 2
        put_response = client.put("/bookings", json=dict(id=res_id))
        assert put_response.status_code == 406
        assert put_response.json["message"] == "Invalid input"
        assert put_response.json["success"] is False
        assert (
            put_response.json["errors"]
            == "'resource_id', 'booked_from' or 'booked_to' JSON arguments should be provided"
        )

    def test_update_with_improper_resource_id_type(self, client):
        """ Update existing booking. """
        res_id = 2
        put_response = client.put("/bookings", json=dict(id=res_id, resource_id="asd"))
        assert put_response.status_code == 406
        assert put_response.json["message"] == "Invalid input"
        assert put_response.json["success"] is False
        assert put_response.json["errors"] == ["'asd' is not of type 'integer'"]

    def test_update_with_improper_booking_from_to_type(self, client):
        """ Update existing booking. """
        # TODO: do zmiany, powinno byc 406 a nie 500 (jsonschema nie waliduje)
        res_id = 2
        put_response = client.put(
            "/bookings", json=dict(id=res_id, booked_from="10AM today")
        )
        assert put_response.status_code == 500
        assert put_response.json["message"] == "Internal server error"
        assert put_response.json["success"] is False
        assert (
            put_response.json["errors"]
            == "ValueError(\"time data '10AM today' does not match format '%Y-%m-%d %H:%M:%S'\",)"
        )

    def test_update_with_improper_filter(self, client):
        """ Try to update booking using improper filter. """
        put_response = client.put(
            "/bookings", json=dict(active=True, title="Adam Malysz")
        )
        assert put_response.status_code == 406
        assert put_response.json["message"] == "Invalid input"
        assert put_response.json["success"] is False
        assert put_response.json["errors"] == ["'id' is a required property"]

    def test_delete_non_existent_booking(self, client):
        """ Try to delete non existent booking. """
        booking_id = 342
        response = client.delete(f"/bookings?id={booking_id}")
        assert response.status_code == 404
        assert response.json["message"] == "Booking not found"
        assert response.json["success"] is False
        assert (
            response.json["errors"]
            == f"Booking with given ID: {booking_id} was not found"
        )

    def test_delete_with_json_body(self, client):
        """ Try to delete booking using unsupported JSON body. """
        res_id = 1
        response = client.delete(f"/bookings", json=dict(id=res_id))
        assert response.status_code == 406
        assert response.json["message"] == "Invalid input"
        assert response.json["success"] is False
        assert response.json["errors"] == "JSON body is not accepted in this endpoint"

    def test_delete_without_args(self, client):
        """ Try to delete booking without URL args. """
        response = client.delete(f"/bookings")
        assert response.status_code == 406
        assert response.json["message"] == "Invalid input"
        assert response.json["success"] is False
        assert response.json["errors"] == "Improper URL parameters provided"

    @classmethod
    def teardown_class(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()
            app.logger.info("Database dropped")
