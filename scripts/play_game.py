"""Main CLI game loop for the RPG."""

import io
import sys
import random
from pathlib import Path
from typing import Optional

# Add src to path FIRST
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Fix Unicode encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from rpg.game.game_state import GameState
from rpg.entities.character import Character
from rpg.entities.item import Item
from rpg.entities.predefined_classes import WARRIOR, MAGE, ROGUE
from rpg.entities.universal_skills import (
    FISHING, MINING, HERBALISM, FORAGING,
    COOKING, ALCHEMY, BLACKSMITHING, TAILORING,
    FIRST_AID, BARTERING, CAMPING, NAVIGATION,
    ALL_UNIVERSAL_SKILLS
)
from rpg.systems.combat import resolve_attack
from rpg.services.shop import ShopService


class RPGGame:
    """Main game controller for the CLI RPG."""
    
    def __init__(self):
        self.game_state: Optional[GameState] = None
        self.running = False
        self.save_path = Path.home() / ".rpg_save.json"
        
    def clear_screen(self):
        """Clear the console screen."""
        print("\n" * 2)
    
    def print_header(self, text: str):
        """Print a formatted header."""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60)
    
    def print_separator(self):
        """Print a separator line."""
        print("-" * 60)
    
    def get_input(self, prompt: str = "> ") -> str:
        """Get user input with prompt."""
        return input(prompt).strip().lower()
    
    def show_main_menu(self):
        """Display the main menu."""
        self.print_header("⚔️  PYTHON RPG - MAIN MENU  ⚔️")
        print("\n1. New Game")
        print("2. Load Game")
        print("3. Quit")
        print()
    
    def create_character(self) -> GameState:
        """Character creation wizard."""
        self.print_header("🎭 CHARACTER CREATION")
        
        # Get name
        print("\nWhat is your name, adventurer?")
        name = input("> ").strip()
        while not name:
            print("Please enter a name!")
            name = input("> ").strip()
        
        # Show class options
        print(f"\nWelcome, {name}! Choose your class:\n")
        
        print("1. WARRIOR")
        print(f"   {WARRIOR.description}")
        print(f"   HP: x{WARRIOR.hp_multiplier} | ATK: +{WARRIOR.attack_bonus} | DEF: +{WARRIOR.defense_bonus}")
        print(f"   Preferred Skills: Mining, Blacksmithing, First Aid\n")
        
        print("2. MAGE")
        print(f"   {MAGE.description}")
        print(f"   HP: x{MAGE.hp_multiplier} | ATK: +{MAGE.attack_bonus} | DEF: {MAGE.defense_bonus}")
        print(f"   Preferred Skills: Herbalism, Alchemy, Navigation\n")
        
        print("3. ROGUE")
        print(f"   {ROGUE.description}")
        print(f"   HP: x{ROGUE.hp_multiplier} | ATK: +{ROGUE.attack_bonus} | DEF: +{ROGUE.defense_bonus}")
        print(f"   Preferred Skills: Foraging, Cooking, Bartering\n")
        
        # Get class choice
        class_choice = ""
        while class_choice not in ["1", "2", "3"]:
            choice = self.get_input("Choose class (1-3): ")
            if choice in ["1", "2", "3"]:
                class_choice = choice
            else:
                print("Invalid choice! Enter 1, 2, or 3.")
        
        class_map = {"1": "warrior", "2": "mage", "3": "rogue"}
        class_name = class_map[class_choice]
        
        # Create game state
        game_state = GameState.new_game(name, class_name)
        
        self.print_header("🌟 CHARACTER CREATED!")
        self.show_character_stats(game_state)
        print("\nPress Enter to begin your adventure...")
        input()
        
        return game_state
    
    def show_character_stats(self, game_state: GameState):
        """Display character statistics."""
        player = game_state.player
        level = game_state.leveling.level(player)
        xp = game_state.leveling.xp(player)
        xp_needed = game_state.leveling.xp_for_next_level(player)
        
        print(f"\n📊 {player.name} - Level {level} {player.character_class.name if player.character_class else 'Adventurer'}")
        print(f"   HP: {player.hp}/{player.max_hp}")
        print(f"   ATK: {player.attack} | DEF: {player.defense}")
        print(f"   XP: {xp}/{xp_needed}")
        print(f"   💰 Gold: ${player.currency}")
        print(f"   📍 Location: {game_state.location.title()}")
    
    def game_loop(self):
        """Main game loop."""
        while self.running:
            self.print_header("🏰 VILLAGE CENTER")
            self.show_character_stats(self.game_state)
            
            print("\nWhat would you like to do?")
            print("1. 🗺️  Explore the wilderness")
            print("2. ⚔️  Training grounds (combat)")
            print("3. 📚 Learn skills")
            print("4. 🎒 Inventory")
            print("5. 🏪 Visit shop")
            print("6. 🏦 Visit bank")
            print("7. 💾 Save game")
            print("8. 🚪 Quit")
            
            choice = self.get_input("\nEnter choice (1-8): ")
            
            if choice == "1":
                self.explore()
            elif choice == "2":
                self.combat_encounter()
            elif choice == "3":
                self.skill_menu()
            elif choice == "4":
                self.inventory_menu()
            elif choice == "5":
                self.shop_menu()
            elif choice == "6":
                self.bank_menu()
            elif choice == "7":
                self.save_game()
            elif choice == "8":
                self.quit_game()
            else:
                print("Invalid choice!")
                input("\nPress Enter to continue...")
    
    def explore(self):
        """Random exploration events."""
        self.print_header("🗺️  EXPLORATION")
        
        events = [
            ("combat", 0.4),
            ("treasure", 0.3),
            ("skill", 0.2),
            ("nothing", 0.1)
        ]
        
        roll = random.random()
        cumulative = 0.0
        event = "nothing"
        
        for event_type, probability in events:
            cumulative += probability
            if roll < cumulative:
                event = event_type
                break
        
        if event == "combat":
            print("\n⚔️  You encounter a monster!")
            input("Press Enter to fight...")
            self.combat_encounter()
        
        elif event == "treasure":
            gold = random.randint(20, 100)
            self.game_state.player.currency += gold
            print(f"\n💰 You found a treasure chest containing ${gold} gold!")
            input("\nPress Enter to continue...")
        
        elif event == "skill":
            skill = random.choice(ALL_UNIVERSAL_SKILLS)
            print(f"\n📚 You discover an opportunity to practice {skill.name}!")
            
            if self.game_state.skills.can_learn(self.game_state.player, skill):
                if not self.game_state.skills.has_learned(self.game_state.player, skill):
                    self.game_state.skills.learn(self.game_state.player, skill)
                    print(f"✨ You learned {skill.name}!")
                else:
                    print(f"You already know {skill.name}.")
            else:
                level_needed = skill.required_level
                if self.game_state.player.character_class and skill.id in self.game_state.player.character_class.preferred_skills:
                    level_needed = max(1, level_needed - 2)
                print(f"You need to be level {level_needed} to learn {skill.name}.")
            
            input("\nPress Enter to continue...")
        
        else:
            print("\n🌲 You wander through the peaceful forest. Nothing happens.")
            input("\nPress Enter to continue...")
        
        self.game_state.turns_played += 1
    
    def combat_encounter(self):
        """Run a combat encounter."""
        self.print_header("⚔️  COMBAT!")
        
        # Generate enemy
        enemy_types = [
            ("Goblin Scout", 40, 6, 2, 15),
            ("Wolf", 50, 8, 3, 20),
            ("Bandit", 60, 10, 4, 30),
            ("Orc Warrior", 80, 12, 5, 50),
        ]
        
        enemy_data = random.choice(enemy_types)
        enemy = Character(
            name=enemy_data[0],
            max_hp=enemy_data[1],
            attack=enemy_data[2],
            defense=enemy_data[3]
        )
        enemy_reward = enemy_data[4]
        
        print(f"\n💀 A wild {enemy.name} appears!")
        print(f"   HP: {enemy.hp}/{enemy.max_hp} | ATK: {enemy.attack} | DEF: {enemy.defense}")
        
        # Combat loop
        turn = 0
        while enemy.is_alive() and self.game_state.player.is_alive():
            turn += 1
            print(f"\n--- Turn {turn} ---")
            print(f"Your HP: {self.game_state.player.hp}/{self.game_state.player.max_hp}")
            print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")
            
            print("\n1. Attack")
            print("2. Flee")
            
            choice = self.get_input("Action: ")
            
            if choice == "2":
                if random.random() < 0.5:
                    print("\n🏃 You fled successfully!")
                    input("\nPress Enter to continue...")
                    return
                else:
                    print("\n❌ Failed to escape!")
            
            # Player attacks
            print(f"\n⚔️  You attack {enemy.name}!")
            damage = resolve_attack(self.game_state.player, enemy)
            print(f"   💥 Dealt {damage} damage!")
            
            if not enemy.is_alive():
                break
            
            # Enemy attacks
            print(f"\n⚔️  {enemy.name} counterattacks!")
            damage = resolve_attack(enemy, self.game_state.player)
            print(f"   💥 You took {damage} damage!")
        
        # Combat resolution
        if not self.game_state.player.is_alive():
            self.print_header("💀 GAME OVER")
            print(f"\nYou were defeated by {enemy.name}...")
            print("Your adventure ends here.")
            input("\nPress Enter to return to main menu...")
            self.running = False
            return
        
        # Victory
        print(f"\n🎉 Victory! {enemy.name} has been defeated!")
        
        # Rewards
        xp_gained = random.randint(10, 30)
        self.game_state.leveling.gain_xp(self.game_state.player, xp_gained)
        self.game_state.player.currency += enemy_reward
        self.game_state.enemies_defeated += 1
        
        print(f"   ✨ Gained {xp_gained} XP!")
        print(f"   💰 Looted ${enemy_reward} gold!")
        
        # Check for level up
        new_level = self.game_state.leveling.level(self.game_state.player)
        print(f"   📊 Current Level: {new_level}")
        
        # Heal player partially
        self.game_state.player.heal(self.game_state.player.max_hp // 4)
        
        input("\nPress Enter to continue...")
    
    def skill_menu(self):
        """Display and manage skills."""
        self.print_header("📚 SKILLS")
        
        learned = self.game_state.skills.list_learned_skills(self.game_state.player)
        available = [s for s in ALL_UNIVERSAL_SKILLS if self.game_state.skills.can_learn(self.game_state.player, s) 
                     and not self.game_state.skills.has_learned(self.game_state.player, s)]
        
        print(f"\n✅ Learned Skills ({len(learned)}):")
        if learned:
            for skill in learned:
                print(f"   - {skill.name} ({skill.category})")
        else:
            print("   None yet!")
        
        print(f"\n📖 Available to Learn ({len(available)}):")
        if available:
            for i, skill in enumerate(available, 1):
                bonus = " ⭐" if self.game_state.player.character_class and skill.id in self.game_state.player.character_class.preferred_skills else ""
                print(f"   {i}. {skill.name} ({skill.category}) - Level {skill.required_level}{bonus}")
            
            print("\nEnter number to learn skill, or 'b' to go back:")
            choice = self.get_input()
            
            if choice.isdigit() and 1 <= int(choice) <= len(available):
                skill = available[int(choice) - 1]
                self.game_state.skills.learn(self.game_state.player, skill)
                print(f"\n✨ You learned {skill.name}!")
        else:
            print("   None available at your level!")
        
        input("\nPress Enter to continue...")
    
    def inventory_menu(self):
        """Display inventory."""
        self.print_header("🎒 INVENTORY")
        
        items = self.game_state.inventory.list_items()
        
        if items:
            print("\nYour items:")
            for item in items:
                equipped = " (Equipped)" if self.game_state.inventory.is_equipped(item.id) else ""
                print(f"   - {item.name}{equipped}")
        else:
            print("\nYour inventory is empty!")
        
        input("\nPress Enter to continue...")
    
    def shop_menu(self):
        """Visit the shop."""
        self.print_header("🏪 VILLAGE SHOP")
        
        # Create shop with items
        shop = ShopService("General Store")
        
        # Add items for sale
        items_for_sale = [
            (Item(id="sword1", name="Iron Sword", equip_attack=10), 150),
            (Item(id="armor1", name="Leather Armor", equip_defense=5), 120),
            (Item(id="potion1", name="Health Potion", heal_amount=30), 50),
            (Item(id="sword2", name="Steel Sword", equip_attack=20), 300),
            (Item(id="armor2", name="Chain Mail", equip_defense=10), 250),
        ]
        
        for item, price in items_for_sale:
            if not self.game_state.inventory.has_item(item.id):
                shop.add_item_for_sale(item, price)
        
        print(f"\nWelcome to {shop.name}!")
        print(f"Your gold: ${self.game_state.player.currency}\n")
        
        inventory = shop.list_inventory()
        if inventory:
            print("Items for sale:")
            for i, (item, price) in enumerate(inventory, 1):
                print(f"   {i}. {item.name} - ${price}")
                if item.equip_attack:
                    print(f"      ATK: +{item.equip_attack}")
                if item.equip_defense:
                    print(f"      DEF: +{item.equip_defense}")
                if item.heal_amount:
                    print(f"      Heals: {item.heal_amount} HP")
            
            print("\nEnter number to buy, or 'b' to go back:")
            choice = self.get_input()
            
            if choice.isdigit() and 1 <= int(choice) <= len(inventory):
                item, price = inventory[int(choice) - 1]
                if shop.sell_item_to(item.id, self.game_state.player, self.game_state.inventory):
                    print(f"\n✅ Purchased {item.name}!")
                    
                    # Auto-equip if it's equipment and better
                    if item.equip_attack or item.equip_defense:
                        self.game_state.inventory.equip(item.id, self.game_state.player)
                        print(f"⚔️  Equipped {item.name}!")
                else:
                    print(f"\n❌ Not enough gold! Need ${price}.")
        else:
            print("No items available for purchase!")
        
        input("\nPress Enter to continue...")
    
    def bank_menu(self):
        """Visit the bank."""
        self.print_header("🏦 VILLAGE BANK")
        
        balance = self.game_state.bank.check_balance(self.game_state.player)
        
        print(f"\nAccount Balance: ${balance}")
        print(f"Gold in hand: ${self.game_state.player.currency}")
        
        print("\n1. Deposit")
        print("2. Withdraw")
        print("3. Back")
        
        choice = self.get_input("\nChoice: ")
        
        if choice == "1":
            if self.game_state.player.currency > 0:
                print(f"\nHow much to deposit? (max ${self.game_state.player.currency})")
                amount_str = self.get_input("Amount: $")
                if amount_str.isdigit():
                    amount = int(amount_str)
                    if self.game_state.bank.deposit_from(self.game_state.player, amount):
                        print(f"✅ Deposited ${amount}")
                    else:
                        print("❌ Invalid amount!")
            else:
                print("\n❌ You have no gold to deposit!")
        
        elif choice == "2":
            if balance > 0:
                print(f"\nHow much to withdraw? (max ${balance})")
                amount_str = self.get_input("Amount: $")
                if amount_str.isdigit():
                    amount = int(amount_str)
                    if self.game_state.bank.withdraw_to(self.game_state.player, amount):
                        print(f"✅ Withdrew ${amount}")
                    else:
                        print("❌ Invalid amount!")
            else:
                print("\n❌ Your account is empty!")
        
        input("\nPress Enter to continue...")
    
    def save_game(self):
        """Save the current game state."""
        self.game_state.save_to_file(self.save_path)
        print("\n💾 Game saved successfully!")
        input("\nPress Enter to continue...")
    
    def load_game(self) -> bool:
        """Load a saved game."""
        if not self.save_path.exists():
            print("\n❌ No saved game found!")
            input("\nPress Enter to continue...")
            return False
        
        try:
            self.game_state = GameState.load_from_file(self.save_path)
            print("\n✅ Game loaded successfully!")
            input("\nPress Enter to continue...")
            return True
        except Exception as e:
            print(f"\n❌ Error loading game: {e}")
            input("\nPress Enter to continue...")
            return False
    
    def quit_game(self):
        """Quit the game."""
        print("\n👋 Thanks for playing!")
        self.running = False
    
    def run(self):
        """Start the game."""
        self.print_header("⚔️  WELCOME TO PYTHON RPG  ⚔️")
        print("\nA text-based adventure with classes, skills, and combat!")
        
        while True:
            self.show_main_menu()
            choice = self.get_input("Enter choice (1-3): ")
            
            if choice == "1":
                # New game
                self.game_state = self.create_character()
                self.running = True
                self.game_loop()
            
            elif choice == "2":
                # Load game
                if self.load_game():
                    self.running = True
                    self.game_loop()
            
            elif choice == "3":
                # Quit
                print("\n👋 Goodbye!")
                break
            
            else:
                print("Invalid choice!")


if __name__ == "__main__":
    game = RPGGame()
    game.run()
