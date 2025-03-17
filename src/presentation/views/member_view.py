import uuid
from typing import Any, Dict

from flask import Response, abort, jsonify, make_response, request
from flask.views import MethodView

from src.application.members_services import MembersService
from src.presentation.errors_handlers.member_errors import MemberErrors


class MembersView(MethodView):
    def __init__(self) -> None:
        self.service = MembersService()

    def get(self, members_id: uuid.UUID | None = None) -> Response:
        if members_id is None:
            members = self.service.get_all()
            return make_response(jsonify(members or []), 200)

        members_id_str = str(members_id)
        member: Dict[str, Any] | None = self.service.get_by_id(
            members_id_str)
        if member is None:
            return MemberErrors.member_not_found()

        return jsonify(member)

    def post(self) -> Response:
        data = request.get_json()
        if not data:
            abort(400, description="Invalid data")

        entity = {
            "name": data.get("name"),
            "email": data.get("email"),
        }
        if not all([entity["name"], entity["email"]]):
            abort(400, description="Required fields missing")

        result = self.service.add(entity)
        if result:
            return make_response(jsonify(result), 201)
        abort(500, description="Error adding member")

    def put(self, members_id: uuid.UUID) -> Response:
        members_id_str = str(members_id)
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid JSON data"}), 400)

        entity = {
            "name": data.get("name"),
            "email": data.get("email"),
        }

        result = self.service.update(members_id_str, entity)
        if not result:
            return make_response(jsonify({"error": "Member not found"}), 404)
        return jsonify(message="Member updated successfully")

    def delete(self, members_id: str) -> Response:
        members_id_str = str(members_id)
        result = self.service.delete(members_id_str)
        if not result:
            return make_response(jsonify({"error": "Member not found"}), 404)

        return jsonify(message="Member deleted successfully")
