from dataclasses import dataclass

from src.domain.base_entity import BaseEntity
from src.domain.models.member_model import MemberModel


@dataclass
class MemberEntity(BaseEntity):
    name: str = ''
    email: str = ''

    def to_model(self) -> MemberModel:
        return MemberModel(**self.__dict__)
