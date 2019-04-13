import pytest

from src.database.models import db, Resources
from bookings_api import app
from tests import helpers


class TestResourcesPositive:
    @classmethod
    def setup_class(cls):
        cls.url_root = "http://127.0.0.1:5000/"
        with app.app_context():
            db.create_all()
            app.logger.info("Database initialized")
            helpers.insert_test_data_into_db_table(Resources)

    @pytest.fixture(scope="module")
    def client(self):
        testing_client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        yield testing_client
        ctx.pop()

    def test_get_all_resources(self, client):
        """
        Test if all resources from resources_data.csv are correctly returned.
        """
        response = client.get("/resources")
        assert response.status_code == 200
        exp_json = [
            {
                "active": True,
                "created_at": "2018-10-10 10:10:10",
                "id": 1,
                "title": "Sample Resource",
                "updated_at": "2018-10-11 10:10:15",
                "intervals": "15",
                "opening_hours_mon": "08:00-12:00-12:30-16:00",
                "opening_hours_tue": "08:00-12:00-12:30-16:00",
                "opening_hours_wed": "08:00-12:00-12:30-16:00",
                "opening_hours_thu": "08:00-12:00-12:30-16:00",
                "opening_hours_fri": "08:00-12:00-12:30-16:00",
                "opening_hours_sat": "",
                "opening_hours_sun": "",
            },
            {
                "active": False,
                "created_at": "2018-10-10 05:05:05",
                "id": 2,
                "title": "Johnny Bravo",
                "updated_at": "2018-11-10 06:06:06",
                "intervals": "30",
                "opening_hours_mon": "08:00-12:00",
                "opening_hours_tue": "08:00-12:00",
                "opening_hours_wed": "08:00-12:00",
                "opening_hours_thu": "08:00-12:00",
                "opening_hours_fri": "08:00-12:00",
                "opening_hours_sat": "08:00-12:00",
                "opening_hours_sun": "",
            },
            {
                "active": True,
                "created_at": "2017-01-03 07:07:07",
                "id": 3,
                "title": "Adam Malysz",
                "updated_at": "2017-02-02 11:12:13",
                "intervals": "60",
                "opening_hours_mon": "",
                "opening_hours_tue": "",
                "opening_hours_wed": "",
                "opening_hours_thu": "",
                "opening_hours_fri": "",
                "opening_hours_sat": "08:00-16:00",
                "opening_hours_sun": "08:00-16:00",
            },
        ]
        assert response.json == exp_json

    def test_get_resource_by_id(self, client):
        """ Get resource by its ID. """
        response = client.get("/resources?id=1")
        exp_json = [
            {
                "active": True,
                "created_at": "2018-10-10 10:10:10",
                "id": 1,
                "title": "Sample Resource",
                "updated_at": "2018-10-11 10:10:15",
                "intervals": "15",
                "opening_hours_mon": "08:00-12:00-12:30-16:00",
                "opening_hours_tue": "08:00-12:00-12:30-16:00",
                "opening_hours_wed": "08:00-12:00-12:30-16:00",
                "opening_hours_thu": "08:00-12:00-12:30-16:00",
                "opening_hours_fri": "08:00-12:00-12:30-16:00",
                "opening_hours_sat": "",
                "opening_hours_sun": "",
            }
        ]
        assert response.status_code == 200
        assert response.json == exp_json

    def test_get_resource_by_title(self, client):
        """ Get resource by its title. """
        response = client.get("/resources?title=Sample Resource")
        exp_json = [
            {
                "active": True,
                "created_at": "2018-10-10 10:10:10",
                "id": 1,
                "title": "Sample Resource",
                "updated_at": "2018-10-11 10:10:15",
                "intervals": "15",
                "opening_hours_mon": "08:00-12:00-12:30-16:00",
                "opening_hours_tue": "08:00-12:00-12:30-16:00",
                "opening_hours_wed": "08:00-12:00-12:30-16:00",
                "opening_hours_thu": "08:00-12:00-12:30-16:00",
                "opening_hours_fri": "08:00-12:00-12:30-16:00",
                "opening_hours_sat": "",
                "opening_hours_sun": "",
            }
        ]
        assert response.status_code == 200
        assert response.json == exp_json

    def test_add_resource(self, client):
        """ Add resource to database. """
        post_response = client.post(
            "/resources",
            json=dict(
                title="Test Resource",
                active=True,
                intervals="30",
                opening_hours_mon="8:30-12:00",
            ),
        )
        assert post_response.status_code == 200
        assert post_response.json["success"] is True
        get_response = client.get("/resources?title=Test Resource")
        assert get_response.json[0]["title"] == "Test Resource"
        assert get_response.json[0]["intervals"] == "30"
        assert get_response.json[0]["opening_hours_mon"] == "8:30-12:00"
        assert get_response.json[0]["id"] == 4

    def test_update_resource(self, client):
        """ Update existing resource. """
        put_response = client.put("/resources", json=dict(id=4, active=False))
        assert put_response.status_code == 200
        get_response = client.get("/resources?id=4")
        assert get_response.json[0]["active"] is False

    def test_delete_resource(self, client):
        """ Delete existing resource using its ID. """
        delete_response = client.delete("/resources?id=4")
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
