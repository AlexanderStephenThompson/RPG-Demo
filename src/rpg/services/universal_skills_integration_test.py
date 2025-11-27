"""Integration tests for universal skills with character classes."""

import pytest
from rpg.entities.character import Character
from rpg.entities.predefined_classes import WARRIOR, MAGE, ROGUE
from rpg.entities.universal_skills import (
    FISHING, MINING, HERBALISM, FORAGING,
    COOKING, ALCHEMY, BLACKSMITHING, TAILORING,
    FIRST_AID, BARTERING, CAMPING, NAVIGATION
)
from rpg.services.leveling import LevelingService
from rpg.services.skills import SkillsService


def test_warrior_prefers_mining_blacksmithing_first_aid() -> None:
    """Warrior gets 2-level reduction on mining, blacksmithing, and first_aid."""
    char = Character("Tank", max_hp=100, character_class=WARRIOR)
    leveling = LevelingService()
    skills = SkillsService(leveling)

    # Mining normally requires level 2, warrior needs level 1 (2 - 2 = 0, clamped to 1)
    assert leveling.level(char) == 1
    assert skills.can_learn(char, MINING)

    # Blacksmithing normally requires level 4, warrior needs level 2 (4 - 2 = 2)
    assert not skills.can_learn(char, BLACKSMITHING)
    leveling.gain_xp(char, 10)  # Get to level 2
    assert leveling.level(char) == 2
    assert skills.can_learn(char, BLACKSMITHING)

    # First Aid normally requires level 2, warrior needs level 1
    char2 = Character("Tank2", max_hp=100, character_class=WARRIOR)
    assert leveling.level(char2) == 1
    assert skills.can_learn(char2, FIRST_AID)


def test_mage_prefers_herbalism_alchemy_navigation() -> None:
    """Mage gets 2-level reduction on herbalism, alchemy, and navigation."""
    char = Character("Wizard", max_hp=50, character_class=MAGE)
    leveling = LevelingService()
    skills = SkillsService(leveling)

    # Herbalism normally requires level 1, mage needs level 1 (1 - 2 = -1, clamped to 1)
    assert leveling.level(char) == 1
    assert skills.can_learn(char, HERBALISM)

    # Alchemy normally requires level 3, mage needs level 1 (3 - 2 = 1)
    assert leveling.level(char) == 1
    assert skills.can_learn(char, ALCHEMY)

    # Navigation normally requires level 4, mage needs level 2 (4 - 2 = 2)
    assert not skills.can_learn(char, NAVIGATION)
    leveling.gain_xp(char, 10)  # Get to level 2
    assert leveling.level(char) == 2
    assert skills.can_learn(char, NAVIGATION)


def test_rogue_prefers_foraging_cooking_bartering() -> None:
    """Rogue gets 2-level reduction on foraging, cooking, and bartering."""
    char = Character("Thief", max_hp=75, character_class=ROGUE)
    leveling = LevelingService()
    skills = SkillsService(leveling)

    # Foraging normally requires level 1, rogue needs level 1 (1 - 2 = -1, clamped to 1)
    assert leveling.level(char) == 1
    assert skills.can_learn(char, FORAGING)

    # Cooking normally requires level 2, rogue needs level 1 (2 - 2 = 0, clamped to 1)
    assert leveling.level(char) == 1
    assert skills.can_learn(char, COOKING)

    # Bartering normally requires level 3, rogue needs level 1 (3 - 2 = 1)
    assert leveling.level(char) == 1
    assert skills.can_learn(char, BARTERING)


def test_all_classes_can_learn_all_universal_skills() -> None:
    """Any class can learn any universal skill (flexible approach)."""
    warrior = Character("Tank", max_hp=100, character_class=WARRIOR)
    mage = Character("Wizard", max_hp=50, character_class=MAGE)
    rogue = Character("Thief", max_hp=75, character_class=ROGUE)
    
    leveling = LevelingService()
    skills = SkillsService(leveling)

    # Level all characters to 5
    for char in [warrior, mage, rogue]:
        leveling.gain_xp(char, 40)  # Gets to level 5

    all_universal = [
        FISHING, MINING, HERBALISM, FORAGING,
        COOKING, ALCHEMY, BLACKSMITHING, TAILORING,
        FIRST_AID, BARTERING, CAMPING, NAVIGATION
    ]

    # All characters can learn all universal skills at level 5
    for char in [warrior, mage, rogue]:
        for skill in all_universal:
            assert skills.can_learn(char, skill)


def test_skill_categories_are_correct() -> None:
    """Verify all universal skills have correct categories."""
    gathering = [FISHING, MINING, HERBALISM, FORAGING]
    crafting = [COOKING, ALCHEMY, BLACKSMITHING, TAILORING]
    utility = [FIRST_AID, BARTERING, CAMPING, NAVIGATION]

    for skill in gathering:
        assert skill.category == "Gathering"

    for skill in crafting:
        assert skill.category == "Crafting"

    for skill in utility:
        assert skill.category == "Utility"
