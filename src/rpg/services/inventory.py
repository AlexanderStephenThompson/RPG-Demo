from __future__ import annotations

from rpg.entities.character import Character
from rpg.entities.item import Item


class InventoryService:
    """Manages a character's collection of items with equip/unequip and consumable usage.

    Service class that handles item management logic for a single character.
    Tracks both available items and currently equipped items separately.
    Equipping modifies character stats directly; unequipping reverses changes.
    """

    def __init__(self) -> None:
        self._items: dict[str, Item] = {}
        self._equipped: dict[str, Item] = {}

    def add(self, item: Item) -> None:
        """Add an item to the inventory by its unique ID."""
        self._items[item.id] = item

    def remove(self, item_id: str) -> Item | None:
        """Remove and return item by ID, or None if not found."""
        return self._items.pop(item_id, None)

    def list_items(self) -> list[Item]:
        """Return a list of all items currently in inventory (excludes equipped items tracking)."""
        return list(self._items.values())

    def equip(self, item_id: str, character: Character) -> bool:
        """Equip an item, applying its stat bonuses to the character.

        Modifies character's attack and defense in-place by adding item bonuses.
        Item must exist in inventory to equip.

        Args:
            item_id: Unique ID of item to equip
            character: Character to receive stat bonuses (modified in-place)

        Returns:
            True if item was equipped, False if item not found in inventory

        Examples:
            >>> character = Character("Hero", max_hp=20, attack=5, defense=2)
            >>> sword = Item(id="sword1", name="Iron Sword", equip_attack=3)
            >>> inventory = InventoryService()
            >>> inventory.add(sword)
            >>> inventory.equip("sword1", character)
            True
            >>> character.attack  # 5 + 3 = 8
            8
        """
        item = self._items.get(item_id)
        if item is None:
            return False
        # apply equip bonuses
        character.attack += item.equip_attack
        character.defense += item.equip_defense
        self._equipped[item_id] = item
        return True

    def unequip(self, item_id: str, character: Character) -> bool:
        """Unequip an item, removing its stat bonuses from the character.

        Reverses stat changes by subtracting item bonuses. Item must be currently equipped.

        Args:
            item_id: Unique ID of equipped item to remove
            character: Character to lose stat bonuses (modified in-place)

        Returns:
            True if item was unequipped, False if item not currently equipped

        Examples:
            >>> character = Character("Hero", max_hp=20, attack=8, defense=2)
            >>> sword = Item(id="sword1", name="Iron Sword", equip_attack=3)
            >>> inventory = InventoryService()
            >>> inventory.add(sword)
            >>> inventory.equip("sword1", character)
            True
            >>> character.attack  # 8 + 3 = 11
            11
            >>> inventory.unequip("sword1", character)
            True
            >>> character.attack  # 11 - 3 = 8 (restored)
            8
        """
        item = self._equipped.pop(item_id, None)
        if item is None:
            return False
        character.attack -= item.equip_attack
        character.defense -= item.equip_defense
        return True

    def use_consumable(self, item_id: str, target: Character) -> bool:
        """Use a consumable item on a target character, then remove it from inventory.

        Applies healing effect if item has heal_amount > 0. Item is consumed (removed) after use.

        Args:
            item_id: Unique ID of consumable item
            target: Character to receive the effect (modified in-place)

        Returns:
            True if item was used and removed, False if item not found or has no consumable effect

        Examples:
            >>> character = Character("Hero", max_hp=50)
            >>> character.take_damage(20)  # hp = 30
            >>> potion = Item(id="potion1", name="Health Potion", heal_amount=15)
            >>> inventory = InventoryService()
            >>> inventory.add(potion)
            >>> inventory.use_consumable("potion1", character)
            True
            >>> character.hp  # 30 + 15 = 45
            45
            >>> inventory.list_items()  # Potion consumed and removed
            []
        """
        item = self._items.get(item_id)
        if item is None:
            return False
        if item.heal_amount > 0:
            target.heal(item.heal_amount)
            # remove consumable after use
            self.remove(item_id)
            return True
        return False
