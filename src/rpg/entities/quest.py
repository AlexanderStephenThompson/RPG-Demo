from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Objective:
    """Represents a single quest objective.

    Attributes:
        id: Unique identifier for the objective.
        description: Human-readable description of the objective.
        completed: Whether the objective has been completed (default False).

    Examples:
        >>> obj = Objective(id="gather_herbs", description="Gather 5 healing herbs")
        >>> obj.id
        'gather_herbs'
        >>> obj.completed
        False
    """
    id: str
    description: str
    completed: bool = False


@dataclass
class Quest:
    """Represents a quest with one or more objectives.

    Attributes:
        id: Unique identifier for the quest.
        name: Human-readable quest name.
        description: Detailed quest description.
        objectives: List of objectives that must be completed.

    Raises:
        ValueError: If id or name is empty, if there are no objectives,
                    or if objective IDs are not unique.

    Examples:
        >>> obj1 = Objective(id="plant_seeds", description="Plant 3 seeds")
        >>> obj2 = Objective(id="water_garden", description="Water the garden")
        >>> quest = Quest(
        ...     id="garden_tutorial",
        ...     name="Growing Your First Garden",
        ...     description="Learn the basics of gardening",
        ...     objectives=[obj1, obj2]
        ... )
        >>> quest.name
        'Growing Your First Garden'
        >>> len(quest.objectives)
        2

        >>> Quest(id="", name="Bad", description="Test", objectives=[obj1])
        Traceback (most recent call last):
        ...
        ValueError: quest id must be non-empty

        >>> Quest(id="q1", name="Bad", description="Test", objectives=[])
        Traceback (most recent call last):
        ...
        ValueError: quest must have at least one objective
    """
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
