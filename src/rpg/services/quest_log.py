from __future__ import annotations

from typing import Dict, Set
from rpg.entities.character import Character
from rpg.entities.quest import Quest


class QuestLogService:
    """Track accepted and completed quests per character (placeholder docstring)."""

    def __init__(self) -> None:
        # Map character id -> quest_id -> set of completed objective ids
        self._quest_progress: Dict[int, Dict[str, Set[str]]] = {}
        # Map character id -> set of accepted quest ids
        self._accepted: Dict[int, Set[str]] = {}
        # Store quest definitions to check completion
        self._quests: Dict[str, Quest] = {}

    def accept(self, character: Character, quest: Quest) -> bool:
        """Accept a quest; return True if newly accepted."""
        key = id(character)
        accepted_set = self._accepted.get(key, set())
        if quest.id in accepted_set:
            return False

        if key not in self._accepted:
            self._accepted[key] = set()
        self._accepted[key].add(quest.id)

        if key not in self._quest_progress:
            self._quest_progress[key] = {}
        self._quest_progress[key][quest.id] = set()
        
        # Store quest definition
        self._quests[quest.id] = quest
        return True

    def complete_objective(self, character: Character, quest_id: str, objective_id: str) -> bool:
        """Mark an objective complete; return True if state changed."""
        key = id(character)
        progress = self._quest_progress.get(key, {})
        if quest_id not in progress:
            return False

        # Validate objective exists in quest
        if quest_id not in self._quests:
            return False
        quest = self._quests[quest_id]
        valid_objective_ids = {obj.id for obj in quest.objectives}
        if objective_id not in valid_objective_ids:
            return False

        completed_objectives = progress[quest_id]
        before = len(completed_objectives)
        completed_objectives.add(objective_id)
        return len(completed_objectives) > before

    def is_completed(self, character: Character, quest_id: str) -> bool:
        """Return True if all quest objectives are complete."""
        key = id(character)
        if quest_id not in self._quests:
            return False
        
        quest = self._quests[quest_id]
        progress = self._quest_progress.get(key, {})
        if quest_id not in progress:
            return False
        
        completed_objectives = progress[quest_id]
        all_objective_ids = {obj.id for obj in quest.objectives}
        return all_objective_ids == completed_objectives

    def active(self, character: Character) -> list[str]:
        """Return list of active (not completed) quest IDs."""
        key = id(character)
        accepted_set = self._accepted.get(key, set())
        return [qid for qid in accepted_set if not self.is_completed(character, qid)]

    def completed(self, character: Character) -> list[str]:
        """Return list of completed quest IDs."""
        key = id(character)
        accepted_set = self._accepted.get(key, set())
        return [qid for qid in accepted_set if self.is_completed(character, qid)]
