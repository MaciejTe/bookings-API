import pytest

from src.database.models import db, Users
from bookings_api import app
from tests import helpers


class TestUsersNegative:
    @classmethod
    def setup_class(cls):
        cls.url_root = "http://127.0.0.1:5000/"
        with app.app_context():
            db.create_all()
            app.logger.info("Database initialized")
            helpers.insert_test_data_into_db_table(Users)

    @pytest.fixture(scope="module")
    def client(self):
        testing_client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        yield testing_client
        ctx.pop()

    def test_get_non_existent_user_by_id(self, client):
        """ Provide non existent user ID to search for. """
        response = client.get("/users?id=123")
        assert response.json == []
        assert response.status_code == 200

    def test_get_non_existent_user_by_name(self, client):
        """ Search for non existent user by title. """
        response = client.get("/users?name=Andrzej Golota")
        assert response.json == []
        assert response.status_code == 200

    def test_get_non_existent_user_by_name_and_id(self, client):
        """ Search for non existent user by both title and id. """
        response = client.get("/users?name=Andrzej Golota&id=1")
        assert response.json == []
        assert response.status_code == 200

    def test_get_user_with_json(self, client):
        """ Try to filter GET results with JSON body. """
        response = client.get("/users", json=dict(id=1))
        assert response.status_code == 406
        assert response.json["errors"] == "JSON body is not accepted in this endpoint"
        assert response.json["success"] is False

    def test_get_user_with_improper_filter(self, client):
        """ Use improper filter in GET /users. """
        response = client.get("/users?asd=123s")
        exp_json = [
            {
                "created_at": "2018-10-10 10:10:10",
                "email": "user1@gmail.com",
                "id": 1,
                "name": "User 1",
                "phonenumber": "123456789",
                "updated_at": "2018-10-11 10:10:15",
            },
            {
                "created_at": "2018-10-10 05:05:05",
                "email": "user2@gmail.com",
                "id": 2,
                "name": "User 2",
                "phonenumber": "12730731",
                "updated_at": "2018-11-10 06:06:06",
            },
            {
                "created_at": "2017-01-03 07:07:07",
                "email": "user3@gmail.com",
                "id": 3,
                "name": "User 3",
                "phonenumber": "129402823",
                "updated_at": "2017-02-02 11:12:13",
            },
        ]
        assert response.status_code == 200
        assert response.json == exp_json

    def test_improper_key_when_adding_user(self, client):
        """ Use improper JSON key in POST request. """
        post_response = client.post("/users", json=dict(asd="Janusz"))
        assert post_response.status_code == 406
        assert post_response.json["success"] is False
        assert post_response.json["message"] == "Invalid input"
        assert post_response.json["errors"] == [
            "'name' is a required property",
            "'email' is a required property",
            "'phonenumber' is a required property",
        ]

    def test_update_non_existent_user(self, client):
        """ Update non existent user. """
        user_id = 671
        put_response = client.put(
            "/users", json=dict(id=user_id, email="whatever@domain.com")
        )
        assert put_response.status_code == 404
        assert put_response.json["message"] == "User not found"
        assert put_response.json["success"] is False
        assert (
            put_response.json["errors"]
            == f"User with given ID: {user_id} was not found"
        )

    def test_update_without_params(self, client):
        """ Try to update user without parameters to update. """
        res_id = 2
        put_response = client.put("/users", json=dict(id=res_id))
        assert put_response.status_code == 406
        assert put_response.json["message"] == "Invalid input"
        assert put_response.json["success"] is False
        assert (
            put_response.json["errors"]
            == "'name', 'email' or 'phonenumber' JSON arguments should be provided"
        )

    def test_update_with_improper_active_type(self, client):
        """ Update existing user. """
        res_id = 2
        put_response = client.put("/users", json=dict(id=res_id, name=79))
        assert put_response.status_code == 406
        assert put_response.json["message"] == "Invalid input"
        assert put_response.json["success"] is False
        assert put_response.json["errors"] == ["79 is not of type 'string'"]

    def test_update_with_improper_filter(self, client):
        """ Try to update user using improper filter. """
        put_response = client.put("/users", json=dict(active=True, title="Adam Malysz"))
        assert put_response.status_code == 406
        assert put_response.json["message"] == "Invalid input"
        assert put_response.json["success"] is False
        assert put_response.json["errors"] == ["'id' is a required property"]

    def test_delete_non_existent_user(self, client):
        """ Try to delete non existent user. """
        user_id = 404
        response = client.delete(f"/users?id={user_id}")
        assert response.status_code == 404
        assert response.json["message"] == "User not found"
        assert response.json["success"] is False
        assert response.json["errors"] == f"User with given ID: {user_id} was not found"

    def test_delete_with_json_body(self, client):
        """ Try to delete user using unsupported JSON body. """
        res_id = 1
        response = client.delete(f"/users", json=dict(id=res_id))
        assert response.status_code == 406
        assert response.json["message"] == "Invalid input"
        assert response.json["success"] is False
        assert response.json["errors"] == "JSON body is not accepted in this endpoint"

    def test_delete_without_args(self, client):
        """ Try to delete user without URL args. """
        response = client.delete(f"/resources")
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
