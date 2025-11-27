"""Game state management for the RPG."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from rpg.entities.character import Character
from rpg.entities.predefined_classes import WARRIOR, MAGE, ROGUE
from rpg.services.inventory import InventoryService
from rpg.services.leveling import LevelingService
from rpg.services.skills import SkillsService
from rpg.services.quest_log import QuestLogService
from rpg.services.achievements import AchievementsService
from rpg.services.bank import BankService


@dataclass
class GameState:
    """Manages the complete state of the game."""
    
    player: Character
    inventory: InventoryService
    leveling: LevelingService
    skills: SkillsService
    quests: QuestLogService
    achievements: AchievementsService
    bank: BankService
    
    # Game progression
    location: str = "village"
    turns_played: int = 0
    enemies_defeated: int = 0
    
    @classmethod
    def new_game(cls, player_name: str, character_class_choice: str) -> GameState:
        """Create a new game with a fresh character.
        
        Args:
            player_name: Name for the player character
            character_class_choice: "warrior", "mage", or "rogue"
        
        Returns:
            New GameState with initialized services
        """
        # Select class
        class_map = {
            "warrior": WARRIOR,
            "mage": MAGE,
            "rogue": ROGUE
        }
        char_class = class_map.get(character_class_choice.lower())
        
        # Create player with class bonuses applied
        player = Character(
            name=player_name,
            max_hp=100,
            attack=5,
            defense=3,
            character_class=char_class
        )
        player.currency = 100  # Starting money
        
        # Initialize services
        inventory = InventoryService()
        leveling = LevelingService()
        skills = SkillsService(leveling)
        quests = QuestLogService()
        achievements = AchievementsService()
        bank = BankService("Village Bank")
        
        return cls(
            player=player,
            inventory=inventory,
            leveling=leveling,
            skills=skills,
            quests=quests,
            achievements=achievements,
            bank=bank,
            location="village",
            turns_played=0,
            enemies_defeated=0
        )
    
    def save_to_file(self, filepath: Path) -> None:
        """Save game state to JSON file."""
        # Note: This is a simplified save system
        # A full implementation would need custom serialization for all services
        save_data = {
            "player_name": self.player.name,
            "player_hp": self.player.hp,
            "player_max_hp": self.player.max_hp,
            "player_attack": self.player.attack,
            "player_defense": self.player.defense,
            "player_currency": self.player.currency,
            "player_class": self.player.character_class.id if self.player.character_class else None,
            "location": self.location,
            "turns_played": self.turns_played,
            "enemies_defeated": self.enemies_defeated,
        }
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(save_data, f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: Path) -> GameState:
        """Load game state from JSON file."""
        with open(filepath, "r") as f:
            save_data = json.load(f)
        
        # Reconstruct character with class
        class_map = {
            "warrior": WARRIOR,
            "mage": MAGE,
            "rogue": ROGUE
        }
        char_class = class_map.get(save_data["player_class"]) if save_data["player_class"] else None
        
        # Create player (class bonuses already applied in saved stats)
        player = Character(
            name=save_data["player_name"],
            max_hp=save_data["player_max_hp"],
            attack=save_data["player_attack"],
            defense=save_data["player_defense"],
            character_class=None  # Don't reapply bonuses
        )
        player.hp = save_data["player_hp"]
        player.currency = save_data["player_currency"]
        player.character_class = char_class  # Restore class reference without reapplying bonuses
        
        # Reinitialize services (in a full game, these would be saved too)
        inventory = InventoryService()
        leveling = LevelingService()
        skills = SkillsService(leveling)
        quests = QuestLogService()
        achievements = AchievementsService()
        bank = BankService("Village Bank")
        
        return cls(
            player=player,
            inventory=inventory,
            leveling=leveling,
            skills=skills,
            quests=quests,
            achievements=achievements,
            bank=bank,
            location=save_data["location"],
            turns_played=save_data["turns_played"],
            enemies_defeated=save_data["enemies_defeated"]
        )
