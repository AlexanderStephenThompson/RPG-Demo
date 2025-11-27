from rpg.entities.character import Character
from rpg.entities.skill import Skill
from rpg.entities.classes import WARRIOR, MAGE
from rpg.services.leveling import LevelingService
from rpg.services.skills import SkillsService


def test_mage_learns_preferred_skill_at_reduced_level():
    # Fireball is preferred for mages, should require lower level
    mage = Character("Wizard", max_hp=50, character_class=MAGE)
    leveling = LevelingService()
    skills = SkillsService(leveling)
    
    # Fireball normally requires level 5, but mage can learn at level 3
    fireball = Skill(id="fireball", name="Fireball", required_level=5)
    
    # At level 1, mage cannot learn
    assert leveling.level(mage) == 1
    assert skills.can_learn(mage, fireball) is False
    
    # Gain XP to reach level 3
    leveling.gain_xp(mage, 25)  # Gets to level 3
    assert leveling.level(mage) == 3
    
    # Mage CAN learn fireball at level 3 (2 levels early)
    assert skills.can_learn(mage, fireball) is True
    assert skills.learn(mage, fireball) is True


def test_warrior_learns_non_preferred_skill_at_normal_level():
    # Warrior trying to learn fireball needs the full level requirement
    warrior = Character("Fighter", max_hp=100, character_class=WARRIOR)
    leveling = LevelingService()
    skills = SkillsService(leveling)
    
    fireball = Skill(id="fireball", name="Fireball", required_level=5)
    
    # At level 3, warrior cannot learn (not preferred)
    leveling.gain_xp(warrior, 25)
    assert leveling.level(warrior) == 3
    assert skills.can_learn(warrior, fireball) is False
    
    # At level 5, warrior CAN learn (meets full requirement)
    leveling.gain_xp(warrior, 20)  # Gets to level 5
    assert leveling.level(warrior) == 5
    assert skills.can_learn(warrior, fireball) is True


def test_warrior_learns_preferred_skill_at_reduced_level():
    # Sword Mastery is preferred for warriors
    warrior = Character("Knight", max_hp=100, character_class=WARRIOR)
    leveling = LevelingService()
    skills = SkillsService(leveling)
    
    sword_mastery = Skill(id="sword_mastery", name="Sword Mastery", required_level=4)
    
    # Warrior can learn at level 2 (2 levels early)
    leveling.gain_xp(warrior, 12)
    assert leveling.level(warrior) == 2
    assert skills.can_learn(warrior, sword_mastery) is True


def test_classless_character_no_skill_bonuses():
    # Character without class learns all skills at normal level
    generic = Character("Generic", max_hp=50)
    leveling = LevelingService()
    skills = SkillsService(leveling)
    
    fireball = Skill(id="fireball", name="Fireball", required_level=5)
    
    # At level 3, cannot learn
    leveling.gain_xp(generic, 25)
    assert leveling.level(generic) == 3
    assert skills.can_learn(generic, fireball) is False
    
    # At level 5, can learn
    leveling.gain_xp(generic, 20)
    assert leveling.level(generic) == 5
    assert skills.can_learn(generic, fireball) is True
