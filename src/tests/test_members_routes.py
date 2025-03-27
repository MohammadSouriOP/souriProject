import uuid
from unittest.mock import patch


def test_get_all_members(client):
    with patch('src.application.members_services.MembersService.get_all',
               return_value=[
                   {'id': str(uuid.uuid4()), 'name': 'John Doe',
                    'email': 'john@example.com'}
               ]):
        response = client.get('/members/')
        assert response.status_code == 200


def test_get_member_by_id(client):
    member_id = str(uuid.uuid4())
    with patch('src.application.members_services.MembersService.get_by_id',
               return_value={
                   'id': member_id, 'name': 'John Doe',
                   'email': 'john@example.com'
               }):
        response = client.get(f'/members/{member_id}')
        assert response.status_code == 200


def test_add_member(client):
    member_data = {'name': 'Alice', 'email': 'alice@example.com'}
    with patch('src.application.members_services.MembersService.add',
               return_value={
                   'id': str(uuid.uuid4()), **member_data
               }):
        response = client.post('/members/', json=member_data)
        assert response.status_code == 201


def test_update_member(client):
    member_id = str(uuid.uuid4())
    with patch('src.application.members_services.MembersService.update',
               return_value=True):
        response = client.put(
            f'/members/{member_id}', json={'name': 'Updated', 'email':
                                           'updated@example.com'})
        assert response.status_code == 200


def test_delete_member(client):
    member_id = str(uuid.uuid4())
    with patch('src.application.members_services.MembersService.delete',
               return_value=True):
        response = client.delete(f'/members/{member_id}')
        assert response.status_code == 200
