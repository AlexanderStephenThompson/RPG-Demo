from __future__ import annotations

from typing import Dict, Set
from rpg.entities.character import Character
from rpg.entities.skill import Skill
from rpg.services.leveling import LevelingService


class SkillsService:
    """Manage learned skills per character.

    Rules:
    - Skill may be learned if character level >= ``skill.required_level``.
    - Duplicate learn attempts are ignored (returns False).
    - Identity-based storage using ``id(character)`` (not persistent).

    Examples:
        >>> from rpg.entities.character import Character
        >>> from rpg.entities.skill import Skill
        >>> from rpg.services.leveling import LevelingService
        >>> hero = Character("Hero", max_hp=20)
        >>> leveling = LevelingService()
        >>> skills = SkillsService(leveling)
        >>> fireball = Skill(id="fireball", name="Fireball", required_level=2)
        >>> skills.can_learn(hero, fireball)
        False
        >>> leveling.gain_xp(hero, 12)  # level 1 -> 2 (10 threshold) carry 2 xp
        >>> leveling.level(hero)
        2
        >>> skills.can_learn(hero, fireball)
        True
        >>> skills.learn(hero, fireball)
        True
        >>> skills.learn(hero, fireball)  # duplicate
        False
        >>> skills.learned(hero)
        {'fireball'}
    """

    def __init__(self, leveling: LevelingService | None = None) -> None:
        self._learned: Dict[int, Set[str]] = {}
        self._leveling = leveling or LevelingService()

    def learned(self, character: Character) -> Set[str]:
        """Return a copy of skill ids learned by ``character``."""
        return set(self._learned.get(id(character), set()))

    def can_learn(self, character: Character, skill: Skill) -> bool:
        """Return True if character meets the level requirement for ``skill``."""
        return self._leveling.level(character) >= skill.required_level

    def learn(self, character: Character, skill: Skill) -> bool:
        """Attempt to learn ``skill``; return True only if newly added.

        Returns:
            bool: True if skill newly learned; False if requirement not met or already learned.
        """
        if not self.can_learn(character, skill):
            return False
        key = id(character)
        bucket = self._learned.get(key)
        if bucket is None:
            bucket = set[str]()  # explicit element type
            self._learned[key] = bucket
        before = len(bucket)
        bucket.add(skill.id)
        return len(bucket) > before
