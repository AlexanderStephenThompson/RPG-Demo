from __future__ import annotations

from typing import List, Tuple

from rpg.entities.character import Character
from rpg.entities.item import Item
from rpg.services.inventory import InventoryService


class ShopService:
    """Service for managing a shop where characters can buy items with currency.
    
    Handles shop inventory with items and their prices. Manages purchase transactions
    including currency validation and item transfer to character's inventory service.
    
    Attributes:
        name: Shop's display name
    """
    
    def __init__(self, name: str) -> None:
        """Initialize a new shop with the given name.
        
        Args:
            name: Shop's display name
        """
        self.name = name
        self._inventory: dict[str, Tuple[Item, int]] = {}
    
    def add_item_for_sale(self, item: Item, price: int) -> None:
        """Add an item to the shop's inventory for sale.
        
        Args:
            item: Item to sell
            price: Price in dollars (currency)
            
        Examples:
            >>> shop = ShopService("Armory")
            >>> sword = Item(id="sword1", name="Iron Sword", equip_attack=5)
            >>> shop.add_item_for_sale(sword, price=100)
            >>> len(shop.list_inventory())
            1
        """
        self._inventory[item.id] = (item, price)
    
    def list_inventory(self) -> List[Tuple[Item, int]]:
        """Return list of all items for sale with their prices.
        
        Returns:
            List of tuples containing (Item, price)
        """
        return list(self._inventory.values())
    
    def sell_item_to(self, item_id: str, buyer: Character, buyer_inventory: InventoryService) -> bool:
        """Sell an item from shop inventory to a buyer.
        
        Transfers item to buyer's inventory service and deducts currency if buyer has sufficient funds.
        Item is removed from shop inventory after successful sale.
        
        Args:
            item_id: Unique ID of item to sell
            buyer: Character purchasing the item (modified in-place if successful)
            buyer_inventory: Buyer's inventory service to receive the item
            
        Returns:
            True if sale successful, False if item not in stock or buyer has insufficient funds
            
        Examples:
            >>> shop = ShopService("Potion Shop")
            >>> character = Character("Hero", max_hp=50)
            >>> character.add_currency(100)
            >>> inventory = InventoryService()
            >>> potion = Item(id="potion1", name="Health Potion", heal_amount=20)
            >>> shop.add_item_for_sale(potion, price=50)
            >>> shop.sell_item_to("potion1", character, inventory)
            True
            >>> character.currency
            50
            >>> len(inventory.list_items())
            1
        """
        if item_id not in self._inventory:
            return False
        
        item, price = self._inventory[item_id]
        
        if not buyer.remove_currency(price):
            return False
        
        buyer_inventory.add(item)
        del self._inventory[item_id]
        return True
