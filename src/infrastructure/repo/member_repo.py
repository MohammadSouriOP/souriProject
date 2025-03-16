import uuid
from typing import Dict, List, Optional

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from src.infrastructure.database.schema import members


class MembersRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Dict]:
        query = select(members)
        result = self.session.execute(query)
        return [dict(row) for row in result.mappings().all()]

    def get_by_id(self, members_id: str) -> Optional[Dict]:
        query = select(members).where(
            members.c.members_id == uuid.UUID(members_id))
        result = self.session.execute(query).mappings().first()
        return dict(result) if result else None

    def add(self, member_data: Dict) -> Optional[Dict]:
        member_data["members_id"] = uuid.uuid4()
        query = insert(members).values(
            members_id=member_data.get("members_id"),
            name=member_data["name"],
            email=member_data["email"]
        ).returning(members)
        result = self.session.execute(query)
        inserted_member = result.mappings().first()
        self.session.commit()
        return dict(inserted_member) if inserted_member else None

    def update(self, members_id: str, member_data: Dict) -> Optional[Dict]:
        query = update(members).where(
            members.c.members_id == members_id).values(
            name=member_data.get("name"),
            email=member_data.get("email")
        ).returning(members)
        result = self.session.execute(query)
        updated_member = result.mappings().first()
        self.session.commit()
        return dict(updated_member) if updated_member else None

    def delete(self, members_id: str) -> bool:
        query = delete(members).where(members.c.members_id == members_id)
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0
