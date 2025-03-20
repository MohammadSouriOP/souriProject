import uuid
from dataclasses import dataclass, field

from src.domain.base_entity import BaseEntity


@dataclass
class MemberEntity(BaseEntity):
    name: str = ''
    email: str = ''
    # member_id: uuid.UUID = field(default_factory=uuid.uuid4)
