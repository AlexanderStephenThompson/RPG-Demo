from __future__ import annotations

from typing import Dict, Set
from rpg.entities.character import Character


class AchievementsService:
    """Track earned achievements per character (placeholder docstring)."""

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
            bucket = set()
            self._earned[key] = bucket
        before = len(bucket)
        bucket.add(achievement_id)
        return len(bucket) > before

    def record_purchase(self, character: Character, purchase_success: bool) -> bool:
        """Record a purchase event; award FIRST_PURCHASE_ID on first success."""
        if not purchase_success:
            return False
        if self.FIRST_PURCHASE_ID in self.earned(character):
            return False
        return self._award(character, self.FIRST_PURCHASE_ID)

    def record_quest_completion(self, character: Character, is_first: bool) -> bool:
        """Record quest completion; award QUEST_NOVICE_ID on first completion."""
        if not is_first:
            return False
        if self.QUEST_NOVICE_ID in self.earned(character):
            return False
        return self._award(character, self.QUEST_NOVICE_ID)
