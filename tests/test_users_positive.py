import pytest

from src.database.models import db, Users
from bookings_api import app
from tests import helpers


class TestUsersPositive:
    @classmethod
    def setup_class(cls):
        cls.url_root = "http://127.0.0.1:5000/"
        with app.app_context():
            db.create_all()
            app.logger.info("Database initialized")
            helpers.insert_test_data_into_db_table(Users)

    @pytest.fixture(scope="module")
    def client(self):
        """ Fixture returning Flask testing client.

        Returns:
            testing_client (Flask):
        """
        testing_client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        yield testing_client
        ctx.pop()

    def test_get_all_resources(self, client):
        """
        Test if all resources from resources_data.csv are correctly returned.
        """
        response = client.get("/users")
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

    def test_get_user_by_id(self, client):
        """ Get user by his ID. """
        response = client.get("/users?id=1")
        exp_json = [
            {
                "id": 1,
                "name": "User 1",
                "created_at": "2018-10-10 10:10:10",
                "updated_at": "2018-10-11 10:10:15",
                "email": "user1@gmail.com",
                "phonenumber": "123456789",
            }
        ]
        assert response.status_code == 200
        assert response.json == exp_json

    def test_get_user_by_name(self, client):
        """ Get user by his name. """
        response = client.get("/users?name=User 3")
        exp_json = [
            {
                "created_at": "2017-01-03 07:07:07",
                "email": "user3@gmail.com",
                "id": 3,
                "name": "User 3",
                "phonenumber": "129402823",
                "updated_at": "2017-02-02 11:12:13",
            }
        ]
        assert response.status_code == 200
        assert response.json == exp_json

    def test_get_user_by_id_and_name(self, client):
        """ Get user by his id and name. """
        response = client.get("/users?name=User 3&id=3")
        exp_json = [
            {
                "created_at": "2017-01-03 07:07:07",
                "email": "user3@gmail.com",
                "id": 3,
                "name": "User 3",
                "phonenumber": "129402823",
                "updated_at": "2017-02-02 11:12:13",
            }
        ]
        assert response.status_code == 200
        assert response.json == exp_json

    def test_add_user(self, client):
        """ Add user to database. """
        post_response = client.post(
            "/users",
            json=dict(
                name="Test User", email="testmail@gmail.com", phonenumber="666666666"
            ),
        )
        assert post_response.status_code == 200
        assert post_response.json["success"] is True
        get_response = client.get("/users?name=Test User")
        assert get_response.json[0]["name"] == "Test User"
        assert get_response.json[0]["id"] == 4
        assert get_response.json[0]["email"] == "testmail@gmail.com"
        assert get_response.json[0]["phonenumber"] == "666666666"

    def test_update_user(self, client):
        """ Update existing user. """
        put_response = client.put("/users", json=dict(id=4, phonenumber="123421"))
        assert put_response.status_code == 200
        get_response = client.get("/users?id=4")
        assert get_response.json[0]["phonenumber"] == "123421"

    def test_delete_user(self, client):
        """ Delete existing user using his ID. """
        delete_response = client.delete("/users?id=4")
        assert delete_response.status_code == 200
        assert delete_response.json["success"] is True
        get_response = client.get("/users?id=4")
        assert get_response.json == []
        assert get_response.status_code == 200

    @classmethod
    def teardown_class(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()
            app.logger.info("Database dropped")
