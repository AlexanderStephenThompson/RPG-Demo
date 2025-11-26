class _FixedRng:
    def __init__(self, value: float):
        self._value = value

    def random(self) -> float:
        return self._value


from rpg.entities.character import Character
from rpg.systems.combat import resolve_attack


def test_basic_attack_applies_damage():
    attacker = Character("A", max_hp=20, attack=6)
    defender = Character("D", max_hp=15, defense=2)
    damage = resolve_attack(attacker, defender)
    assert damage == 4
    assert defender.hp == 11


def test_critical_hit_doubles_damage_with_rng():
    attacker = Character("Critter", max_hp=20, attack=8)
    defender = Character("Target", max_hp=20, defense=1)
    random_provider = _FixedRng(0.1)
    damage = resolve_attack(attacker, defender, random_provider=random_provider, crit_chance=0.5)
    assert damage == (8 - 1) * 2
    assert defender.hp == 20 - damage
