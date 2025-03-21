from dataclasses import dataclass

from src.domain.base_entity import BaseEntity


@dataclass
class MemberEntity(BaseEntity):
    name: str = ''
    email: str = ''
