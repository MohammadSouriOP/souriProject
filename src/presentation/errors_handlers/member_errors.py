from flask import jsonify


class MemberErrors:
    @staticmethod
    def member_not_found():
        return jsonify({'error': 'Member not found'}), 404

    @staticmethod
    def email_already_exists():
        return jsonify({'error': 'Email already exists'}), 400

    @staticmethod
    def database_error():
        return jsonify({'error': 'Database error'}), 500

    @staticmethod
    def unknown_error():
        return jsonify({'error': 'Something went wrong'}), 500

    @staticmethod
    def invalid_uuid():
        return jsonify({'error': 'Invalid UUID format'}), 400
