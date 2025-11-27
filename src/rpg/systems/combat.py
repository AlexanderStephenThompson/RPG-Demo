from __future__ import annotations

from typing import Protocol, runtime_checkable

from rpg.entities.character import Character


@runtime_checkable
class RandomProvider(Protocol):
    """Protocol for injecting deterministic or real randomness into combat calculations.

    Implementations must provide a random() method returning float in [0.0, 1.0).
    Use for dependency injection in tests (e.g., _FixedRng) or runtime (e.g., random.Random).
    """

    def random(self) -> float:  # returns 0.0-1.0
        ...


def resolve_attack(
    attacker: Character,
    defender: Character,
    random_provider: RandomProvider | None = None,
    crit_chance: float = 0.0,
) -> int:
    """Resolve a single attack from attacker to defender.

    Calculates damage as (attacker.attack - defender.defense), minimum 0.
    If random_provider is provided and random roll < crit_chance, damage is doubled.
    Applies damage directly to defender's HP.

    Args:
        attacker: Character performing the attack
        defender: Character receiving damage (modified in-place)
        random_provider: Optional RNG for critical hit calculation
        crit_chance: Probability of critical hit (0.0-1.0), requires random_provider

    Returns:
        The final damage value applied to defender

    Examples:
        Basic attack without crits:
        >>> hero = Character("Hero", max_hp=50, attack=10)
        >>> enemy = Character("Goblin", max_hp=20, defense=3)
        >>> damage = resolve_attack(hero, enemy)
        >>> damage
        7
        >>> enemy.hp
        13
    """
    base = max(0, attacker.attack - defender.defense)
    if random_provider is not None and crit_chance > 0.0:
        try:
            if random_provider.random() < crit_chance:
                base *= 2
        except Exception:
            pass
    damage = int(base)
    defender.take_damage(damage)
    return damage
