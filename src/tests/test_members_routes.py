import json
import uuid
from unittest.mock import patch


def test_get_all_members(client):
    with patch("src.application.members_services.MembersService.get_all",
               return_value=[{"members_id": str(uuid.uuid4()),
                              "name": "John Doe",
                              "email": "john@example.com"}]):
        response = client.get("/members")
        assert response.status_code == 200
        assert isinstance(response.json, list)


def test_get_member_by_id(client):
    member_id = str(uuid.uuid4())

    with patch("src.application.members_services.MembersService.get_by_id",
               return_value={"members_id": member_id, "name": "John Doe",
                             "email": "john@example.com"}):
        response = client.get(f"/members/{member_id}")
        assert response.status_code == 200
        assert response.json["name"] == "John Doe"


def test_get_member_not_found(client):
    member_id = str(uuid.uuid4())

    with patch("src.application.members_services.MembersService.get_by_id",
               return_value=None):
        response = client.get(f"/members/{member_id}")
        assert response.status_code == 404
        assert response.json["error"] == "Member not found"


def test_add_member(client):
    member_data = {"name": "Alice", "email": "alice@example.com"}

    with patch("src.application.members_services.MembersService.add",
               return_value={"members_id": str(uuid.uuid4()), **member_data}):
        response = client.post("/members", data=json.dumps(member_data),
                               content_type="application/json")
        assert response.status_code == 201
        assert response.json["name"] == "Alice"


def test_update_member(client):
    member_id = str(uuid.uuid4())
    updated_data = {"name": "Updated Name", "email": "updated@example.com"}

    with patch("src.application.members_services.MembersService.update",
               return_value=True):
        response = client.put(f"/members/{member_id}",
                              data=json.dumps(updated_data),
                              content_type="application/json")
        assert response.status_code == 200
        assert response.json["message"] == "Member updated successfully"


def test_update_member_not_found(client):
    member_id = str(uuid.uuid4())

    with patch("src.application.members_services.MembersService.update",
               return_value=False):
        response = client.put(f"/members/{member_id}",
                              data=json.dumps({"name": "New"}),
                              content_type="application/json")
        assert response.status_code == 404
        assert response.json["error"] == "Member not found"


def test_delete_member(client):
    member_id = str(uuid.uuid4())

    with patch("src.application.members_services.MembersService.delete",
               return_value=True):
        response = client.delete(f"/members/{member_id}")
        assert response.status_code == 200
        assert response.json["message"] == "Member deleted successfully"


def test_delete_member_not_found(client):
    member_id = str(uuid.uuid4())

    with patch("src.application.members_services.MembersService.delete",
               return_value=False):
        response = client.delete(f"/members/{member_id}")
        assert response.status_code == 404
        assert response.json["error"] == "Member not found"
