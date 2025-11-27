from __future__ import annotations

from typing import Dict, Set
from rpg.entities.character import Character
from rpg.entities.skill import Skill
from rpg.services.leveling import LevelingService


class SkillsService:
    """Manage learned skills per character with class-based bonuses.

    Rules:
    - Skill may be learned if character level >= skill.required_level.
    - If character has a class and skill is in class.preferred_skills,
      level requirement is reduced by class_level_reduction (default 2).
    - Duplicate learn attempts are ignored (returns False).
    - Identity-based storage using id(character) (not persistent).

    Examples:
        Basic skill learning without class:
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
        >>> skills.learned(hero)
        {'fireball'}

        Class bonus reduces level requirement:
        >>> from rpg.entities.predefined_classes import MAGE
        >>> mage = Character("Wizard", max_hp=50, character_class=MAGE)
        >>> fireball_adv = Skill(id="fireball", name="Fireball", required_level=5)
        >>> leveling2 = LevelingService()
        >>> skills2 = SkillsService(leveling2)
        >>> leveling2.gain_xp(mage, 25)  # Level 3
        >>> leveling2.level(mage)
        3
        >>> skills2.can_learn(mage, fireball_adv)  # 5 - 2 = 3 (preferred skill)
        True
    """

    def __init__(self, leveling: LevelingService | None = None, class_level_reduction: int = 2) -> None:
        self._learned: Dict[int, Set[str]] = {}
        self._leveling = leveling or LevelingService()
        self._class_level_reduction = class_level_reduction

    def learned(self, character: Character) -> Set[str]:
        """Return a copy of skill ids learned by ``character``."""
        return set(self._learned.get(id(character), set()))

    def can_learn(self, character: Character, skill: Skill) -> bool:
        """Return True if character meets the level requirement for ``skill``.
        
        If character has a class and the skill is in their preferred list,
        the level requirement is reduced by class_level_reduction (default 2).
        """
        required_level = skill.required_level
        
        # Apply class bonus if skill is preferred
        if character.character_class and skill.id in character.character_class.preferred_skills:
            required_level = max(1, required_level - self._class_level_reduction)
        
        return self._leveling.level(character) >= required_level

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
