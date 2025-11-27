from __future__ import annotations

from typing import Dict, Set
from rpg.entities.character import Character


class AchievementsService:
    """Track earned achievements per character.

    This service manages achievement tracking using identity-based storage.
    Achievements are awarded through event recording methods and persist
    only for the lifetime of the service instance.

    Class Attributes:
        FIRST_PURCHASE_ID: Achievement ID for making first purchase.
        QUEST_NOVICE_ID: Achievement ID for completing first quest.

    Examples:
        >>> from rpg.entities.character import Character
        >>> hero = Character("Hero", max_hp=100)
        >>> achievements = AchievementsService()
        >>> achievements.record_purchase(hero, True)
        True
        >>> AchievementsService.FIRST_PURCHASE_ID in achievements.earned(hero)
        True
        >>> achievements.record_purchase(hero, True)  # Already earned
        False
    """

    FIRST_PURCHASE_ID = "first_purchase"
    QUEST_NOVICE_ID = "quest_novice"

    def __init__(self) -> None:
        self._earned: Dict[int, Set[str]] = {}

    def earned(self, character: Character) -> Set[str]:
        return set(self._earned.get(id(character), set()))

    def _award(self, character: Character, achievement_id: str) -> bool:
        key = id(character)
        bucket = self._earned.get(key)
        if bucket is None:
            bucket = set[str]()
            self._earned[key] = bucket
        before = len(bucket)
        bucket.add(achievement_id)
        return len(bucket) > before

    def record_purchase(self, character: Character, purchase_success: bool) -> bool:
        """Record a purchase event and award first purchase achievement.

        Args:
            character: The character making the purchase.
            purchase_success: Whether the purchase was successful.

        Returns:
            True if the first purchase achievement was newly awarded,
            False if purchase failed or achievement already earned.

        Examples:
            >>> from rpg.entities.character import Character
            >>> hero = Character("Hero", max_hp=50)
            >>> achievements = AchievementsService()
            >>> achievements.record_purchase(hero, False)  # Failed purchase
            False
            >>> achievements.record_purchase(hero, True)  # First success
            True
            >>> achievements.record_purchase(hero, True)  # Already earned
            False
        """
        if not purchase_success:
            return False
        if self.FIRST_PURCHASE_ID in self.earned(character):
            return False
        return self._award(character, self.FIRST_PURCHASE_ID)

    def record_quest_completion(self, character: Character, is_first: bool) -> bool:
        """Record a quest completion and award quest novice achievement.

        Args:
            character: The character completing the quest.
            is_first: Whether this is the character's first quest completion.

        Returns:
            True if the quest novice achievement was newly awarded,
            False if not first completion or achievement already earned.

        Examples:
            >>> from rpg.entities.character import Character
            >>> hero = Character("Hero", max_hp=50)
            >>> achievements = AchievementsService()
            >>> achievements.record_quest_completion(hero, True)  # First quest
            True
            >>> AchievementsService.QUEST_NOVICE_ID in achievements.earned(hero)
            True
            >>> achievements.record_quest_completion(hero, True)  # Already earned
            False
            >>> achievements.record_quest_completion(hero, False)  # Not first
            False
        """
        if not is_first:
            return False
        if self.QUEST_NOVICE_ID in self.earned(character):
            return False
        return self._award(character, self.QUEST_NOVICE_ID)
