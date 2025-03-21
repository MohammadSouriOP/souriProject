import uuid
from typing import Any, Dict, Union

from flask import Response, abort, jsonify, make_response, request
from flask.views import MethodView

from src.application.members_services import MembersService
from src.domain.members_entity import MemberEntity
from src.presentation.errors_handlers.member_errors import MemberErrors


class MembersView(MethodView):
    def __init__(self) -> None:
        self.service = MembersService()

    def get(self, member_id: Union[uuid.UUID, str] = '') -> Response:
        if not member_id:
            members = self.service.get_all()
            return make_response(jsonify(members or []), 200)

        try:
            member_uuid = uuid.UUID(str(member_id))
        except ValueError:
            return MemberErrors.invalid_uuid()

        member: Dict[int, Any] | None = self.service.get_by_id(member_uuid)
        if member is None:
            return MemberErrors.member_not_found()

        return jsonify(member)

    def post(self) -> Response:
        data = request.json
        if not data:
            abort(400, description='Invalid data')

        name = data.get('name', '').strip()
        email = data.get('email', '').strip()

        if not name or not email:
            abort(400, description='Name and email cannot be empty')

        ent = MemberEntity(name=name, email=email)
        result = self.service.add(ent)
        if result:
            return make_response(jsonify(result), 201)
        abort(500, description='Error adding member')

    def put(self, member_id: str) -> Response:
        member_id_str = str(member_id)
        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Invalid JSON data'}), 400)

        entity = {
            'name': data.get('name'),
            'email': data.get('email'),
        }

        result = self.service.update(member_id_str, entity)
        if not result:
            return make_response(jsonify({'error': 'Member not found'}), 404)
        return jsonify(message='Member updated successfully')

    def delete(self, member_id: str) -> Response:
        member_id_str = str(member_id)
        result = self.service.delete(member_id_str)
        if not result:
            return make_response(jsonify({'error': 'Member not found'}), 404)

        return jsonify(message='Member deleted successfully')
