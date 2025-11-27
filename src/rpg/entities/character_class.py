from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CharacterClass:
    """Represents a character class with stat modifiers and skill preferences.

    Classes provide flexible specialization without hard restrictions. They modify
    base stats at character creation and reduce level requirements for preferred skills.

    Attributes:
        id: Unique identifier for the class.
        name: Display name of the class.
        description: Flavor text describing the class playstyle.
        hp_multiplier: Multiplier applied to base max_hp (1.0 = no change).
        attack_bonus: Flat bonus added to base attack stat.
        defense_bonus: Flat bonus added to base defense stat.
        preferred_skills: List of skill IDs that this class learns more easily.

    Raises:
        ValueError: If id or name is empty, or if hp_multiplier is non-positive.

    Examples:
        Creating a warrior-type class:
        >>> warrior = CharacterClass(
        ...     id="warrior",
        ...     name="Warrior",
        ...     description="Tank",
        ...     hp_multiplier=1.5,
        ...     attack_bonus=2,
        ...     preferred_skills=["sword_mastery"]
        ... )
        >>> warrior.hp_multiplier
        1.5
        >>> warrior.attack_bonus
        2

        Validation enforced:
        >>> CharacterClass(id="", name="Bad", description="Test")
        Traceback (most recent call last):
        ...
        ValueError: character class id must be non-empty

        >>> CharacterClass(id="bad", name="Bad", description="Test", hp_multiplier=0)
        Traceback (most recent call last):
        ...
        ValueError: hp_multiplier must be positive
    """
    id: str
    name: str
    description: str
    hp_multiplier: float = 1.0
    attack_bonus: int = 0
    defense_bonus: int = 0
    preferred_skills: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("character class id must be non-empty")
        if not self.name:
            raise ValueError("character class name must be non-empty")
        if self.hp_multiplier <= 0:
            raise ValueError("hp_multiplier must be positive")
