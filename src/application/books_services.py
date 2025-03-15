from src.infrastrucutre.unit_of_work.unit_of_work import UnitOfWork


class BooksService:
    def get_all(self):
        with UnitOfWork() as uow:
            assert uow.repo is not None  # Tell Mypy that repo exists
            return uow.repo.get_all()

    def get_by_id(self, book_id: int):
        with UnitOfWork() as uow:
            assert uow.repo is not None
            return uow.repo.get_by_id(book_id)

    def add(self, book_data: dict):
        with UnitOfWork() as uow:
            assert uow.repo is not None
            result = uow.repo.add(book_data)
            uow.commit()
            return result

    def update(self, book_id: int, book_data: dict):
        with UnitOfWork() as uow:
            assert uow.repo is not None
            result = uow.repo.update(book_id, book_data)
            if result:
                uow.commit()
            return result

    def delete(self, book_id: int):
        with UnitOfWork() as uow:
            assert uow.repo is not None
            result = uow.repo.delete(book_id)
            if result:
                uow.commit()
            return result
