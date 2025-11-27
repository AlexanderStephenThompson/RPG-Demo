from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CharacterClass:
    """Represents a character class with stat modifiers and skill preferences (placeholder docstring)."""
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
