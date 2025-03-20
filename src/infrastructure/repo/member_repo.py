from typing import Dict

from sqlalchemy import select
from sqlalchemy.engine import Connection

from src.domain.members_entity import MemberEntity
from src.infrastructure.database.schema import members
from src.infrastructure.repo.base_repo import BaseRepo


class MembersRepo(BaseRepo[MemberEntity]):
    def __init__(self, connection: Connection) -> None:
        super().__init__(MemberEntity, members)
        self.connection = connection

    def get_by_id(self, id: str, connection: Connection) -> Dict | None:
        query = select(members).where(members.c.id == id)
        result = self.connection.execute(query).first()
        return dict(result._mapping) if result else None
