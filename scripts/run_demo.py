"""Run the RPG demo."""

import io
import sys
from pathlib import Path

# Fix Unicode encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Add src to path so imports work
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the demo
if __name__ == "__main__":
    from rpg.entities.character import Character
    from rpg.entities.item import Item
    from rpg.services.bank import BankService
    from rpg.services.inventory import InventoryService
    from rpg.services.shop import ShopService
    from rpg.systems.combat import resolve_attack

    def main():
        print("=" * 60)
        print("TDD Python RPG - Demo")
        print("=" * 60)

        # Create characters
        hero = Character("Brave Hero", max_hp=100, attack=15, defense=5)
        hero.add_currency(500)
        hero_inventory = InventoryService()
        print(f"\n✨ {hero.name} appears!")
        print(
            f"   HP: {hero.hp}/{hero.max_hp} | ATK: {hero.attack} | DEF: {hero.defense}"
        )
        print(f"   Currency: ${hero.currency}")

        # Visit the shop
        print("=" * 60)
        print("🏪 Visiting the Item Shop...")
        print("=" * 60)

        shop = ShopService("Adventurer's Emporium")
        sword = Item(id="sword1", name="Iron Sword", equip_attack=10)
        armor = Item(id="armor1", name="Leather Armor", equip_defense=5)
        potion = Item(id="potion1", name="Health Potion", heal_amount=30)

        shop.add_item_for_sale(sword, price=200)
        shop.add_item_for_sale(armor, price=150)
        shop.add_item_for_sale(potion, price=50)

        print(f"\nWelcome to {shop.name}!")
        print("Available items:")
        for item, price in shop.list_inventory():
            print(f"  - {item.name}: ${price}")

        # Buy items
        print(f"\n💰 Purchasing {sword.name}...")
        shop.sell_item_to("sword1", hero, hero_inventory)
        print(f"   Currency remaining: ${hero.currency}")

        print(f"\n💰 Purchasing {armor.name}...")
        shop.sell_item_to("armor1", hero, hero_inventory)
        print(f"   Currency remaining: ${hero.currency}")

        # Equip items
        print("\n" + "=" * 60)
        print("⚔️  Equipping gear...")
        print("=" * 60)
        hero_inventory.equip("sword1", hero)
        print(f"Equipped {sword.name}! ATK: {hero.attack}")

        hero_inventory.equip("armor1", hero)
        print(f"Equipped {armor.name}! DEF: {hero.defense}")

        # Visit the bank
        print("\n" + "=" * 60)
        print("🏦 Visiting the Bank...")
        print("=" * 60)

        bank = BankService("First National")
        print(f"\nDepositing ${hero.currency} into {bank.name}...")
        bank.deposit_from(hero, amount=hero.currency)
        print(f"   Bank balance: ${bank.check_balance(hero)}")
        print(f"   Currency in hand: ${hero.currency}")

        # Combat encounter
        print("\n" + "=" * 60)
        print("⚔️  Combat Encounter!")
        print("=" * 60)

        goblin = Character("Goblin Warrior", max_hp=50, attack=8, defense=2)
        print(f"\n💀 A wild {goblin.name} appears!")
        print(
            f"   HP: {goblin.hp}/{goblin.max_hp} | ATK: {goblin.attack} | DEF: {goblin.defense}"
        )

        print(f"\n⚔️  {hero.name} attacks {goblin.name}!")
        damage = resolve_attack(hero, goblin)
        print(
            f"   Dealt {damage} damage! {goblin.name} HP: {goblin.hp}/{goblin.max_hp}"
        )

        print(f"\n⚔️  {goblin.name} counterattacks!")
        damage = resolve_attack(goblin, hero)
        print(f"   Took {damage} damage! {hero.name} HP: {hero.hp}/{hero.max_hp}")

        print(f"\n⚔️  {hero.name} strikes again!")
        damage = resolve_attack(hero, goblin)
        print(
            f"   Dealt {damage} damage! {goblin.name} HP: {goblin.hp}/{goblin.max_hp}"
        )

        if not goblin.is_alive():
            print(f"\n🎉 Victory! {goblin.name} has been defeated!")

        # Final status
        print("\n" + "=" * 60)
        print("📊 Final Status")
        print("=" * 60)
        print(f"\n{hero.name}:")
        print(f"   HP: {hero.hp}/{hero.max_hp}")
        print(f"   ATK: {hero.attack} | DEF: {hero.defense}")
        print(f"   Currency: ${hero.currency}")
        print(f"   Bank Balance: ${bank.check_balance(hero)}")
        print(
            f"   Inventory: {', '.join(item.name for item in hero_inventory.list_items())}"
        )
        print("\n" + "=" * 60)
        print("Demo Complete!")
        print("=" * 60)

    main()
