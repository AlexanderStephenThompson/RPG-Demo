from __future__ import annotations

from typing import Dict, Set
from rpg.entities.character import Character
from rpg.entities.quest import Quest


class QuestLogService:
    """Track accepted and completed quests per character.

    This service manages quest acceptance and objective completion tracking
    using identity-based storage. Quest progress persists only for the
    lifetime of the service instance.

    Examples:
        >>> from rpg.entities.character import Character
        >>> from rpg.entities.quest import Quest, Objective
        >>> hero = Character("Hero", max_hp=100)
        >>> log = QuestLogService()
        >>> obj = Objective(id="talk_to_elder", description="Talk to the village elder")
        >>> quest = Quest(id="q1", name="Village Errand", description="Help the village", objectives=[obj])
        >>> log.accept(hero, quest)
        True
        >>> log.accept(hero, quest)  # Already accepted
        False
        >>> "q1" in log.active(hero)
        True
        >>> log.complete_objective(hero, "q1", "talk_to_elder")
        True
        >>> log.is_completed(hero, "q1")
        True
        >>> "q1" in log.completed(hero)
        True
    """

    def __init__(self) -> None:
        # Map character id -> quest_id -> set of completed objective ids
        self._quest_progress: Dict[int, Dict[str, Set[str]]] = {}
        # Map character id -> set of accepted quest ids
        self._accepted: Dict[int, Set[str]] = {}
        # Store quest definitions to check completion
        self._quests: Dict[str, Quest] = {}

    def accept(self, character: Character, quest: Quest) -> bool:
        """Accept a quest for the character.

        Args:
            character: The character accepting the quest.
            quest: The quest to accept.

        Returns:
            True if the quest was newly accepted, False if already accepted.

        Examples:
            >>> from rpg.entities.character import Character
            >>> from rpg.entities.quest import Quest, Objective
            >>> hero = Character("Hero", max_hp=50)
            >>> log = QuestLogService()
            >>> obj = Objective(id="obj1", description="Do something")
            >>> quest = Quest(id="q1", name="Quest", description="Desc", objectives=[obj])
            >>> log.accept(hero, quest)
            True
            >>> log.accept(hero, quest)
            False
        """
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
        """Mark a quest objective as completed.

        Args:
            character: The character completing the objective.
            quest_id: The ID of the quest containing the objective.
            objective_id: The ID of the objective to complete.

        Returns:
            True if the objective was newly marked complete, False if already
            completed, quest not accepted, or objective ID invalid.

        Examples:
            >>> from rpg.entities.character import Character
            >>> from rpg.entities.quest import Quest, Objective
            >>> hero = Character("Hero", max_hp=50)
            >>> log = QuestLogService()
            >>> obj = Objective(id="obj1", description="Task")
            >>> quest = Quest(id="q1", name="Quest", description="D", objectives=[obj])
            >>> log.accept(hero, quest)
            True
            >>> log.complete_objective(hero, "q1", "obj1")
            True
            >>> log.complete_objective(hero, "q1", "obj1")  # Already done
            False
            >>> log.complete_objective(hero, "q1", "invalid")  # Invalid objective
            False
        """
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
        """Check if all objectives for a quest are completed.

        Args:
            character: The character to check.
            quest_id: The ID of the quest to check.

        Returns:
            True if all objectives are complete, False otherwise.

        Examples:
            >>> from rpg.entities.character import Character
            >>> from rpg.entities.quest import Quest, Objective
            >>> hero = Character("Hero", max_hp=50)
            >>> log = QuestLogService()
            >>> obj1 = Objective(id="obj1", description="Task 1")
            >>> obj2 = Objective(id="obj2", description="Task 2")
            >>> quest = Quest(id="q1", name="Q", description="D", objectives=[obj1, obj2])
            >>> log.accept(hero, quest)
            True
            >>> log.is_completed(hero, "q1")
            False
            >>> log.complete_objective(hero, "q1", "obj1")
            True
            >>> log.is_completed(hero, "q1")
            False
            >>> log.complete_objective(hero, "q1", "obj2")
            True
            >>> log.is_completed(hero, "q1")
            True
        """
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
        """Get all active (incomplete) quest IDs for a character.

        Args:
            character: The character to check.

        Returns:
            List of quest IDs that are accepted but not completed.

        Examples:
            >>> from rpg.entities.character import Character
            >>> from rpg.entities.quest import Quest, Objective
            >>> hero = Character("Hero", max_hp=50)
            >>> log = QuestLogService()
            >>> obj = Objective(id="obj1", description="Task")
            >>> quest = Quest(id="q1", name="Q", description="D", objectives=[obj])
            >>> log.accept(hero, quest)
            True
            >>> log.active(hero)
            ['q1']
            >>> log.complete_objective(hero, "q1", "obj1")
            True
            >>> log.active(hero)
            []
        """
        key = id(character)
        accepted_set = self._accepted.get(key, set())
        return [qid for qid in accepted_set if not self.is_completed(character, qid)]

    def completed(self, character: Character) -> list[str]:
        """Get all completed quest IDs for a character.

        Args:
            character: The character to check.

        Returns:
            List of quest IDs that have all objectives completed.

        Examples:
            >>> from rpg.entities.character import Character
            >>> from rpg.entities.quest import Quest, Objective
            >>> hero = Character("Hero", max_hp=50)
            >>> log = QuestLogService()
            >>> obj = Objective(id="obj1", description="Task")
            >>> quest = Quest(id="q1", name="Q", description="D", objectives=[obj])
            >>> log.accept(hero, quest)
            True
            >>> log.completed(hero)
            []
            >>> log.complete_objective(hero, "q1", "obj1")
            True
            >>> log.completed(hero)
            ['q1']
        """
        key = id(character)
        accepted_set = self._accepted.get(key, set())
        return [qid for qid in accepted_set if self.is_completed(character, qid)]
