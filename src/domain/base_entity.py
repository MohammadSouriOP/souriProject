from dataclasses import dataclass, field
from typing import Any


@dataclass
class BaseEntity:
    id: int | None = field(default=None)

    def update(self, data: dict[str, Any]) -> 'BaseEntity':
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
