"""Predefined character classes."""

from rpg.entities.character_class import CharacterClass


WARRIOR = CharacterClass(
    id="warrior",
    name="Warrior",
    description="A mighty melee combatant with high HP and attack power",
    hp_multiplier=1.5,
    attack_bonus=2,
    defense_bonus=0,
    preferred_skills=[
        # Combat skills
        "sword_mastery",
        "shield_bash",
        # Universal skills
        "mining",
        "blacksmithing",
        "first_aid"
    ]
)

MAGE = CharacterClass(
    id="mage",
    name="Mage",
    description="A spellcaster with reduced HP but powerful magic abilities",
    hp_multiplier=0.8,
    attack_bonus=0,
    defense_bonus=-1,
    preferred_skills=[
        # Combat skills
        "fireball",
        "heal",
        "ice_shard",
        # Universal skills
        "herbalism",
        "alchemy",
        "navigation"
    ]
)

ROGUE = CharacterClass(
    id="rogue",
    name="Rogue",
    description="A versatile adventurer balanced in combat and utility skills",
    hp_multiplier=1.0,
    attack_bonus=1,
    defense_bonus=1,
    preferred_skills=[
        # Combat skills
        "lockpicking",
        "sneak",
        "backstab",
        # Universal skills
        "foraging",
        "cooking",
        "bartering"
    ]
)
