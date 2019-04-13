import pytest

from src.database.models import db, Resources
from bookings_api import app
from tests import helpers


class TestResourcesNegative:
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

    def test_get_non_existent_resource_by_id(self, client):
        """
        Provide non existent user ID to search for.
        """
        response = client.get("/resources?id=123")
        assert response.json == []
        assert response.status_code == 200

    def test_get_non_existent_resource_by_title(self, client):
        """ Search for non existent resource by title. """
        response = client.get("/resources?title=Andrzej Golota")
        assert response.json == []
        assert response.status_code == 200

    def test_get_non_existent_resource_by_title_and_id(self, client):
        """ Search for non existent resource by both title and id. """
        response = client.get("/resources?title=Andrzej Golota&id=1")
        assert response.json == []
        assert response.status_code == 200

    def test_get_resource_with_json(self, client):
        """ Try to filter GET results with JSON body. """
        response = client.get("/resources", json=dict(id=1))
        assert response.status_code == 406
        assert response.json["errors"] == "JSON body is not accepted in this endpoint"
        assert response.json["success"] is False

    def test_get_resource_with_improper_filter(self, client):
        """ Use improper filter in GET /resources. """
        response = client.get("/resources?asd=123s")
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
        assert response.status_code == 200
        assert response.json == exp_json

    def test_improper_key_when_adding_resource(self, client):
        """ Use improper JSON key in POST request. """
        post_response = client.post("/resources", json=dict(asd="Janusz"))
        assert post_response.status_code == 406
        assert post_response.json["success"] is False
        assert post_response.json["message"] == "Invalid input"
        assert post_response.json["errors"] == [
            "'active' is a required property",
            "'title' is a required property",
        ]

    def test_update_non_existent_resource(self, client):
        """ Update existing resource. """
        res_id = 671
        put_response = client.put("/resources", json=dict(id=res_id, active=False))
        assert put_response.status_code == 404
        assert put_response.json["message"] == "Resource not found"
        assert put_response.json["success"] is False
        assert (
            put_response.json["errors"]
            == f"Resource with given ID: {res_id} was not found"
        )

    def test_update_with_improper_value(self, client):
        """ Try to update resource using improper value (title cannot be updated). """
        res_id = 2
        put_response = client.put("/resources", json=dict(id=res_id, title="Sample"))
        assert put_response.status_code == 406
        assert put_response.json["message"] == "Invalid input"
        assert put_response.json["success"] is False
        assert put_response.json["errors"] == ["'active' is a required property"]

    def test_update_with_improper_active_type(self, client):
        """ Update existing resource. """
        res_id = 2
        put_response = client.put("/resources", json=dict(id=res_id, active="Sample"))
        assert put_response.status_code == 406
        assert put_response.json["message"] == "Invalid input"
        assert put_response.json["success"] is False
        assert put_response.json["errors"] == ["'Sample' is not of type 'boolean'"]

    def test_update_with_improper_filter(self, client):
        """ Try to update resource using improper filter. """
        put_response = client.put(
            "/resources", json=dict(active=True, title="Adam Malysz")
        )
        assert put_response.status_code == 403
        assert put_response.json["message"] == "Unsupported filter"
        assert put_response.json["success"] is False
        assert (
            put_response.json["errors"]
            == "ID is the only supported filter at this moment"
        )

    def test_delete_non_existent_resource(self, client):
        """ Try to delete non existent resource. """
        res_id = 404
        response = client.delete(f"/resources?id={res_id}")
        assert response.status_code == 404
        assert response.json["message"] == "Resource not found"
        assert response.json["success"] is False
        assert (
            response.json["errors"] == f"Resource with given ID: {res_id} was not found"
        )

    def test_delete_with_json_body(self, client):
        """ Try to delete resource using unsupported JSON body. """
        res_id = 1
        response = client.delete(f"/resources", json=dict(id=res_id))
        assert response.status_code == 406
        assert response.json["message"] == "Invalid input"
        assert response.json["success"] is False
        assert response.json["errors"] == "JSON body is not accepted in this endpoint"

    def test_delete_without_args(self, client):
        """ Try to delete resources without URL args. """
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
