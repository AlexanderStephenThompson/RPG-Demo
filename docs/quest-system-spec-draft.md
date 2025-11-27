# Quest System Spec (Draft - Pending Approval)

Do not implement yet. This captures the initial proposal for a **basic quest system** to enable narrative progression and structured objectives.

## Goal (Smallest Valuable Slice)
Provide per-character quest tracking supporting:
1. Accepting a quest (unique id) with one or more objectives.
2. Marking an objective complete.
3. Determining if a quest is complete (all objectives done).
4. Preventing duplicate acceptance of the same quest.
5. Listing active vs completed quests.

## Out of Scope (For Now)
- Rewards distribution (can be added later via AchievementsService or separate RewardsService).
- Time limits, branching, failure states.
- Objective types (kill, collect, talk) are abstract; we only store descriptions.
- Persistence beyond in-memory identity-based structures.

## Core Domain Model (Proposed)
```python
@dataclass
class Objective:
	id: str
	description: str
	completed: bool = False

@dataclass
class Quest:
	id: str
	name: str
	objectives: list[Objective]
```

Validation rules:
- Quest must have at least one objective.
- All ids non-empty.
- Duplicate objective ids within a single quest are invalid.

## Service API (QuestLogService)
```python
class QuestLogService:
	def accept(self, character: Character, quest: Quest) -> bool: ...  # True if newly accepted
	def complete_objective(self, character: Character, quest_id: str, objective_id: str) -> bool: ...  # True if state changed
	def is_completed(self, character: Character, quest_id: str) -> bool: ...
	def active(self, character: Character) -> list[str]: ...  # quest ids
	def completed(self, character: Character) -> list[str]: ...  # quest ids
```

Storage: identity-based (`id(character)`) mapping to quest state (objectives marked) mirroring existing services (LevelingService, SkillsService).

## Smallest Next Behavior (Initial Test Target)
Accept a single-objective quest, mark objective complete, quest becomes completed.

### Test Name (Happy Path)
`test_accept_and_complete_single_objective_quest`

### Given
- New character
- Quest with id `q_gather`, one objective `o_collect`

### When
- Accept quest
- Complete objective

### Then
- `accept` returns True
- Quest appears in `active` then moves to `completed` after completion
- `is_completed` becomes True

### Edge Test (Duplicate Acceptance)
`test_cannot_accept_same_quest_twice`
Given quest already accepted → second `accept` returns False; quest count unchanged.

## Open Questions (Need User Clarification)
1. Should objectives be automatically completed via external events later (event bus), or only manual for now? (Assuming manual now.)
2. Should quest completion trigger an achievement automatically (e.g., first quest complete)? (Defer unless requested.)
3. Do we need ordering enforcement for objectives (sequence) or just any order? (Assuming any order.)
4. Should partial progress for an objective exist (e.g., count toward target) or binary only? (Binary only for initial slice.)
5. Error behavior: silent False vs raising exceptions on invalid objective/quest ids? (Propose returning False for missing ids to keep domain gentle.)
6. Are quest ids globally unique across all characters? (Assuming yes.)

## Failure Mode Expectations (RED)
- Calling `is_completed` before marking objective returns False.
- Completing non-existent objective returns False (no state change).
- Second `accept` returns False.

## Branch Suggestion
Branch name on approval: `feature/basic-quest-system`

## Next Step
Await answers to Open Questions + approval. Then create branch, write failing tests, proceed with Red → Green.

---
Please review and confirm or adjust scope/questions.
