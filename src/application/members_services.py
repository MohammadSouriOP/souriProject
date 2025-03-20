import uuid

from src.domain.members_entity import MemberEntity
from src.infrastructure.unit_of_work.unit_of_work import UnitOfWork


class MembersService:
    def get_all(self):
        with UnitOfWork() as uow:
            return uow.members_repo.get_all(uow.connection)

    def get_by_id(self, member_id: uuid.UUID):
        with UnitOfWork() as uow:
            return uow.members_repo.get(str(member_id), uow.connection)

    def add(self, member_data: MemberEntity):
        with UnitOfWork() as uow:
            result = uow.members_repo.create(member_data, uow.connection)
            uow.commit()
            return result

    def update(self, member_id: str, member_data: dict):
        with UnitOfWork() as uow:
            result = uow.members_repo.update(
                str(member_id), member_data, uow.connection)
            if not result:
                print("Update failed, transaction might be inactive.")
                return False
            if result:
                uow.commit()
            return result

    def delete(self, member_id: str):
        with UnitOfWork() as uow:
            result = uow.members_repo.delete(str(member_id), uow.connection)
            if result:
                uow.commit()
            return result
