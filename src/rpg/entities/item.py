from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Item:
    """Represents an equippable or consumable game item.

    Pure domain entity - contains only item data and properties.
    Does not manage equipping logic (delegated to InventoryService).

    Attributes:
        id: Unique identifier for this item instance
        name: Display name
        equip_attack: Attack bonus when equipped (0 if not equippable)
        equip_defense: Defense bonus when equipped (0 if not equippable)
        heal_amount: HP restored when consumed (0 if not consumable)

    Examples:
        >>> sword = Item("sword_1", "Iron Sword", equip_attack=5)
        >>> sword.name
        'Iron Sword'
        >>> sword.equip_attack
        5
        >>> sword.equip_defense
        0

        >>> shield = Item("shield_1", "Wooden Shield", equip_defense=3)
        >>> shield.equip_defense
        3

        >>> potion = Item("potion_1", "Health Potion", heal_amount=20)
        >>> potion.heal_amount
        20
    """

    id: str
    name: str
    equip_attack: int = 0
    equip_defense: int = 0
    heal_amount: int = 0
