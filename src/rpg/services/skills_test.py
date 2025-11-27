from rpg.entities.character import Character
from rpg.entities.skill import Skill
from rpg.services.leveling import LevelingService
from rpg.services.skills import SkillsService


def test_learn_skill_with_level_requirement():
    hero = Character("Hero", max_hp=30)
    leveling = LevelingService()
    skills = SkillsService(leveling)

    fireball = Skill(id="fireball", name="Fireball", required_level=2)

    # Initially cannot learn
    assert leveling.level(hero) == 1
    assert skills.can_learn(hero, fireball) is False
    assert skills.learn(hero, fireball) is False

    # Gain XP to reach level 2
    leveling.gain_xp(hero, 15)  # thresholds 10 → lvl2, carry 5
    assert leveling.level(hero) == 2

    # Now can learn
    assert skills.can_learn(hero, fireball) is True
    assert skills.learn(hero, fireball) is True
    assert skills.learned(hero) == {"fireball"}

    # Learning again returns False and doesn't duplicate
    assert skills.learn(hero, fireball) is False
    assert skills.learned(hero) == {"fireball"}
