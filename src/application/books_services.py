from src.infrastructure.unit_of_work.unit_of_work import UnitOfWork


class BooksService:
    def get_all(self):
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            return uow.books_repo.get_all()

    def get_by_id(self, book_id: int):
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            return uow.books_repo.get_by_id(book_id)

    def add(self, book_data: dict):
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            result = uow.books_repo.add(book_data)
            uow.commit()
            return result

    def update(self, book_id: int, book_data: dict):
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            result = uow.books_repo.update(book_id, book_data)
            if result:
                uow.commit()
            return result

    def delete(self, book_id: int):
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            result = uow.books_repo.delete(book_id)
            if result:
                uow.commit()
            return result
