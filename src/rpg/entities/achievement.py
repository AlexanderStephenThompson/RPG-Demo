from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Achievement:
    """Represents a single achievement definition (placeholder docstring)."""
    id: str
    name: str
    description: str

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("achievement id must be non-empty")
        if not self.name:
            raise ValueError("achievement name must be non-empty")
        if not self.description:
            raise ValueError("achievement description must be non-empty")
