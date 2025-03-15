from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class BaseEntity:
    id: Optional[int]

    def update(self, data: dict[str, Any]) -> 'BaseEntity':
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
