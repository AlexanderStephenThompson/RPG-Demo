"""Predefined universal (life) skills organized by category.

Universal skills are non-combat abilities that any character class can learn.
They are organized into three categories:
- Gathering: Resource collection skills
- Crafting: Item creation and enhancement skills
- Utility: Survival and social skills
"""

from rpg.entities.skill import Skill

# Gathering Skills - Resource collection
FISHING = Skill(
    id="fishing",
    name="Fishing",
    required_level=1,
    category="Gathering"
)

MINING = Skill(
    id="mining",
    name="Mining",
    required_level=2,
    category="Gathering"
)

HERBALISM = Skill(
    id="herbalism",
    name="Herbalism",
    required_level=1,
    category="Gathering"
)

FORAGING = Skill(
    id="foraging",
    name="Foraging",
    required_level=1,
    category="Gathering"
)

# Crafting Skills - Item creation
COOKING = Skill(
    id="cooking",
    name="Cooking",
    required_level=2,
    category="Crafting"
)

ALCHEMY = Skill(
    id="alchemy",
    name="Alchemy",
    required_level=3,
    category="Crafting"
)

BLACKSMITHING = Skill(
    id="blacksmithing",
    name="Blacksmithing",
    required_level=4,
    category="Crafting"
)

TAILORING = Skill(
    id="tailoring",
    name="Tailoring",
    required_level=3,
    category="Crafting"
)

# Utility Skills - Survival and social
FIRST_AID = Skill(
    id="first_aid",
    name="First Aid",
    required_level=2,
    category="Utility"
)

BARTERING = Skill(
    id="bartering",
    name="Bartering",
    required_level=3,
    category="Utility"
)

CAMPING = Skill(
    id="camping",
    name="Camping",
    required_level=2,
    category="Utility"
)

NAVIGATION = Skill(
    id="navigation",
    name="Navigation",
    required_level=4,
    category="Utility"
)

# Category collections for convenience
GATHERING_SKILLS = [FISHING, MINING, HERBALISM, FORAGING]
CRAFTING_SKILLS = [COOKING, ALCHEMY, BLACKSMITHING, TAILORING]
UTILITY_SKILLS = [FIRST_AID, BARTERING, CAMPING, NAVIGATION]

ALL_UNIVERSAL_SKILLS = GATHERING_SKILLS + CRAFTING_SKILLS + UTILITY_SKILLS
