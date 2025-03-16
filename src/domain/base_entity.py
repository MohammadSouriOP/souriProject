from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class BaseEntity:
    id: Optional[int] = field(default=None)

    def update(self, data: dict[str, Any]) -> 'BaseEntity':
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
