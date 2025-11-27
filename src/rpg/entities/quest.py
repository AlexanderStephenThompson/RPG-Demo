from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Objective:
    """Represents a single quest objective (placeholder docstring)."""
    id: str
    description: str
    completed: bool = False


@dataclass
class Quest:
    """Represents a quest with objectives (placeholder docstring)."""
    id: str
    name: str
    description: str
    objectives: list[Objective] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("quest id must be non-empty")
        if not self.name:
            raise ValueError("quest name must be non-empty")
        if not self.objectives:
            raise ValueError("quest must have at least one objective")
        # Check for duplicate objective IDs
        obj_ids = [obj.id for obj in self.objectives]
        if len(obj_ids) != len(set(obj_ids)):
            raise ValueError("quest objectives must have unique ids")
