from typing import Any, Generic, List, Type, TypeVar

from sqlalchemy import Table, delete, insert, select, update
from sqlalchemy.engine import Connection

from src.domain.base_entity import BaseEntity

E = TypeVar('E', bound=BaseEntity)


class BaseRepo(Generic[E]):
    def __init__(self, entity: Type[E], table: Table) -> None:
        self.entity = entity
        self.table = table

    def create(self, entity: E, connection: Connection) -> E | None:
        data = {key: value for key, value in
                vars(entity).items() if key != 'id'}
        if not data:
            return None

        sql = insert(self.table).values(**data).returning(*self.table.columns)

        try:
            result = connection.execute(sql)
            inserted_row = result.first()
            return self.entity(**inserted_row._mapping
                               ) if inserted_row else None
        except InterruptedError as e:
            if 'duplicate key value violates unique constraint' in str(e):
                raise ValueError('''
                    The email address is already in use,
                    Please try another one.
                    ''')
            raise

    def get_all(self, connection: Connection) -> List[E]:
        sql = select(self.table)
        result = connection.execute(sql)
        return [self.entity(**row._mapping) for row in result.fetchall()]

    def get(self, id: str, connection: Connection) -> E | None:
        sql = select(self.table).where(self.table.c.id == id)
        result = connection.execute(sql).first()
        return self.entity(**result._mapping) if result else None

    def update(self, id: str, entity_data: dict[str, Any],
               connection: Connection) -> bool:
        sql = update(self.table).where(
            self.table.c.id == id).values(**entity_data)
        result = connection.execute(sql)
        return result.rowcount > 0

    def delete(self, id: str, connection: Connection) -> bool:
        sql = delete(self.table).where(self.table.c.id == id)
        result = connection.execute(sql)
        return result.rowcount > 0
