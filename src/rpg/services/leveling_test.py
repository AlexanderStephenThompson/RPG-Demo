from rpg.entities.character import Character
from rpg.services.leveling import LevelingService


def test_gain_xp_and_level_up_at_threshold():
    hero = Character("Hero", max_hp=30, attack=5, defense=2)
    svc = LevelingService()

    assert svc.level(hero) == 1
    assert svc.xp(hero) == 0

    # Gain XP to just before threshold
    svc.gain_xp(hero, 9)
    assert svc.level(hero) == 1
    assert svc.xp(hero) == 9

    # Threshold is 10 → levels to 2 and carries remainder
    svc.gain_xp(hero, 3)
    assert svc.level(hero) == 2
    assert svc.xp(hero) == 2


def test_multiple_levels_with_carry_and_no_negative_inputs():
    hero = Character("Hero", max_hp=30)
    svc = LevelingService()

    # Large XP grants can cross multiple levels; threshold scales linearly
    svc.gain_xp(hero, 25)  # 10 → lvl2 (carry 15), 20 → lvl3 (carry -5 → 10 carry)
    assert svc.level(hero) == 3
    assert svc.xp(hero) == 5  # Explanation: 25 - 10 - 10 = 5 (thresholds 10, then 10)

    # Reject negative XP
    try:
        svc.gain_xp(hero, -1)
        assert False, "negative xp should raise"
    except ValueError:
        pass


def test_next_threshold_and_progress_ratio():
    hero = Character("Hero", max_hp=30)
    svc = LevelingService()

    svc.gain_xp(hero, 7)
    assert svc.next_threshold(hero) == 10
    assert 0.69 < svc.progress_ratio(hero) < 0.71  # 7/10 ≈ 0.7
