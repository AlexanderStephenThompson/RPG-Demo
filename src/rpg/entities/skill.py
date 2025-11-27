from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Skill:
    """Represents a learnable skill with a name and level requirement.

    Pure entity: data + validation only.

    Attributes:
        id: Stable identifier
        name: Display name
        required_level: Minimum character level to learn (>=1)
        category: Optional category for organization (e.g., "Gathering", "Crafting", "Utility")

    Examples:
        Basic creation:
        >>> fireball = Skill(id="fireball", name="Fireball", required_level=2)
        >>> fireball.name
        'Fireball'
        >>> fireball.required_level
        2

        With category:
        >>> fishing = Skill(id="fishing", name="Fishing", required_level=1, category="Gathering")
        >>> fishing.category
        'Gathering'

        Validation rules:
        >>> Skill(id="s1", name="Slash", required_level=1).required_level
        1
        >>> from pytest import raises
        >>> with raises(ValueError):  # required_level must be >= 1
        ...     Skill(id="bad", name="Broken", required_level=0)
    """

    id: str
    name: str
    required_level: int = 1
    category: str = ""

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("skill id must be non-empty")
        if not self.name:
            raise ValueError("skill name must be non-empty")
        if self.required_level < 1:
            raise ValueError("required_level must be >= 1")
