from rpg.entities.item import Item
from rpg.entities.character import Character
from rpg.services.inventory import InventoryService


def test_add_and_remove_item():
    inventory = InventoryService()
    potion = Item(id="p1", name="Potion", heal_amount=5)
    inventory.add(potion)
    items = inventory.list_items()
    assert len(items) == 1
    assert items[0].id == "p1"
    removed = inventory.remove("p1")
    assert removed is not None
    assert inventory.list_items() == []


def test_equip_and_unequip_changes_stats():
    character = Character("Hero", max_hp=20, attack=3, defense=1)
    sword = Item(id="s1", name="Sword", equip_attack=4)
    inventory = InventoryService()
    inventory.add(sword)
    equipped = inventory.equip("s1", character)
    assert equipped
    assert character.attack == 7
    unequipped = inventory.unequip("s1", character)
    assert unequipped
    assert character.attack == 3


def test_use_consumable_heals_and_removes():
    character = Character("Healed", max_hp=20)
    character.take_damage(8)
    inventory = InventoryService()
    potion = Item(id="p1", name="Potion", heal_amount=5)
    inventory.add(potion)
    assert inventory.use_consumable("p1", character)
    assert character.hp == 17
    assert inventory.list_items() == []
