from __future__ import annotations

from typing import Dict
from rpg.entities.character import Character


class LevelingService:
    """Track per-character XP and levels.

    Rules:
    - All characters start at level 1 with 0 XP.
    - Level threshold is currently a constant 10 XP per level (demo simplification).
    - XP carries over after leveling up (excess applied to next level).
    - Negative XP gains raise ``ValueError``.
    - Storage uses ``id(character)`` (identity-based, not persistent across reloads).

    Examples:
        Basic leveling and carry-over:
        >>> from rpg.entities.character import Character
        >>> hero = Character("Hero", max_hp=20)
        >>> lvl = LevelingService()
        >>> lvl.level(hero), lvl.xp(hero)
        (1, 0)
        >>> lvl.gain_xp(hero, 9)   # below threshold
        >>> lvl.level(hero), lvl.xp(hero)
        (1, 9)
        >>> lvl.gain_xp(hero, 3)   # 9+3 = 12 → level 2 with 2 carry
        >>> lvl.level(hero), lvl.xp(hero)
        (2, 2)

        Multiple level ups in one grant:
        >>> hero2 = Character("Mage", max_hp=18)
        >>> lvl.gain_xp(hero2, 25)  # levels 1→2 (10), 2→3 (10), 5 carry
        >>> lvl.level(hero2), lvl.xp(hero2)
        (3, 5)

        Validation:
        >>> from pytest import raises
        >>> with raises(ValueError):
        ...     lvl.gain_xp(hero, -1)
    """

    def __init__(self) -> None:
        self._xp: Dict[int, int] = {}
        self._level: Dict[int, int] = {}

    def level(self, character: Character) -> int:
        """Return the current level for ``character`` (defaults to 1)."""
        return self._level.get(id(character), 1)

    def xp(self, character: Character) -> int:
        """Return current accumulated XP toward next level (defaults to 0)."""
        return self._xp.get(id(character), 0)

    def next_threshold(self, character: Character) -> int:
        """Return XP required for next level (constant 10 for demo)."""
        return 10

    def progress_ratio(self, character: Character) -> float:
        """Return fraction (0.0–1.0) of progress toward next level."""
        return self.xp(character) / float(self.next_threshold(character))

    def gain_xp(self, character: Character, amount: int) -> None:
        """Add XP to ``character`` and apply level-ups with carry-over.

        Args:
            character: Target character whose XP/level is tracked.
            amount: Non-negative XP amount to add.

        Raises:
            ValueError: If ``amount`` is negative.
        """
        if amount < 0:
            raise ValueError("xp amount must be non-negative")
        key = id(character)
        current_xp = self._xp.get(key, 0) + int(amount)
        current_level = self._level.get(key, 1)

        # Process leveling with carry-over
        threshold = self.next_threshold(character)
        while current_xp >= threshold:
            current_xp -= threshold
            current_level += 1
        self._xp[key] = current_xp
        self._level[key] = current_level
