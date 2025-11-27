import pytest

from rpg.entities.character import Character
from rpg.entities.item import Item
from rpg.services.inventory import InventoryService
from rpg.services.shop import ShopService


def test_shop_creation():
    shop = ShopService(name="General Store")
    assert shop.name == "General Store"
    assert shop.list_inventory() == []


def test_add_item_for_sale():
    shop = ShopService(name="Armory")
    sword = Item(id="sword1", name="Iron Sword", equip_attack=5)
    shop.add_item_for_sale(sword, price=100)
    inventory = shop.list_inventory()
    assert len(inventory) == 1
    assert inventory[0][0].id == "sword1"
    assert inventory[0][1] == 100


def test_sell_item_to_success():
    shop = ShopService(name="Potion Shop")
    character = Character("Hero", max_hp=50)
    character.add_currency(150)
    inventory = InventoryService()

    potion = Item(id="potion1", name="Health Potion", heal_amount=20)
    shop.add_item_for_sale(potion, price=50)

    result = shop.sell_item_to("potion1", character, inventory)
    assert result is True
    assert character.currency == 100
    assert len(inventory.list_items()) == 1
    assert inventory.list_items()[0].id == "potion1"


def test_sell_item_to_insufficient_funds():
    shop = ShopService(name="Expensive Shop")
    character = Character("Poor Hero", max_hp=50)
    character.add_currency(25)
    inventory = InventoryService()

    sword = Item(id="sword1", name="Iron Sword", equip_attack=5)
    shop.add_item_for_sale(sword, price=100)

    result = shop.sell_item_to("sword1", character, inventory)
    assert result is False
    assert character.currency == 25
    assert len(inventory.list_items()) == 0


def test_sell_item_to_not_in_stock():
    shop = ShopService(name="Empty Shop")
    character = Character("Rich Hero", max_hp=50)
    character.add_currency(500)
    inventory = InventoryService()

    result = shop.sell_item_to("nonexistent", character, inventory)
    assert result is False
    assert character.currency == 500


def test_sell_item_to_removes_from_shop():
    shop = ShopService(name="One Item Shop")
    character = Character("Buyer", max_hp=50)
    character.add_currency(100)
    inventory = InventoryService()

    armor = Item(id="armor1", name="Leather Armor", equip_defense=3)
    shop.add_item_for_sale(armor, price=75)

    shop.sell_item_to("armor1", character, inventory)
    assert len(shop.list_inventory()) == 0
