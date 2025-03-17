from src.infrastructure.unit_of_work.unit_of_work import UnitOfWork


class MembersService:
    def get_all(self):
        with UnitOfWork() as uow:
            assert uow.members_repo is not None
            return uow.members_repo.get_all()

    def get_by_id(self, member_id: str):
        with UnitOfWork() as uow:
            assert uow.members_repo is not None
            return uow.members_repo.get_by_id(member_id)

    def add(self, member_data: dict):
        with UnitOfWork() as uow:
            assert uow.members_repo is not None
            result = uow.members_repo.add(member_data)
            uow.commit()
            return result

    def update(self, member_id: str, member_data: dict):
        with UnitOfWork() as uow:
            assert uow.members_repo is not None
            result = uow.members_repo.update(member_id, member_data)
            if result:
                uow.commit()
            return result

    def delete(self, member_id: str):
        with UnitOfWork() as uow:
            assert uow.members_repo is not None
            result = uow.members_repo.delete(member_id)
            if result:
                uow.commit()
            return result
