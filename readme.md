# TDD Python RPG

A playable console-based Python RPG built strictly following Test-Driven Development and design patterns. Features clean architecture with domain-driven design for maximum clarity and maintainability.

## 🎮 How to Play

```powershell
# Start the game
C:/Users/Alexa/AppData/Local/Programs/Python/Python313/python.exe scripts\play_game.py
```

**Game Features:**
- Create a character with one of three classes (Warrior, Mage, Rogue)
- Explore the wilderness and encounter random events
- Engage in turn-based combat with monsters
- Learn universal skills (Gathering, Crafting, Utility)
- Buy and equip items from the shop
- Save and load your progress
- Gain XP and level up your character

## Features

### Character System
- ⚔️ **Character Classes** - Warrior, Mage, Rogue with flexible specialization
  - Stat modifiers (HP, attack, defense) applied at creation
  - Skill preferences reduce level requirements without hard restrictions
  - Any class can learn any skill or equip any item
- 📊 **Leveling System** - XP-based progression with carry-over mechanics
- 🎓 **Skills System** - Level-gated skill learning with class bonuses
- 🛠️ **Universal Skills** - 12 life skills across 3 categories
  - **Gathering**: Fishing, Mining, Herbalism, Foraging
  - **Crafting**: Cooking, Alchemy, Blacksmithing, Tailoring
  - **Utility**: First Aid, Bartering, Camping, Navigation

### Combat & Items
- ⚔️ **Combat System** - Turn-based combat with critical hits
- 🎒 **Inventory Management** - Equip items to modify stats dynamically
- 🗡️ **Equipment** - Weapons and armor with stat bonuses

### Economy
- 🏪 **Shop System** - Buy/sell items with currency
- 🏦 **Banking** - Deposit, withdraw, transfer between accounts
- 💰 **Currency** - Character wallet and bank balance tracking

### Progression & Goals
- 🎯 **Quest System** - Accept quests, complete objectives, track progress
- 🏆 **Achievements** - Unlock achievements for milestones
- 🌱 **Gardening Skill** - Tutorial quest introduces specialized skills

## Project Structure

```
src/rpg/
├── entities/          # Pure domain models (data + validation)
│   ├── character.py   # Character with class integration
│   ├── character_class.py  # Class definition entity
│   ├── predefined_classes.py  # Warrior, Mage, Rogue
│   ├── skill.py       # Skill entity with category field
│   ├── universal_skills.py  # 12 life skills (Gathering, Crafting, Utility)
│   ├── item.py        # Equipment and consumables
│   ├── quest.py       # Quest and Objective entities
│   └── achievement.py
├── services/          # Business logic
│   ├── leveling.py    # XP and level tracking
│   ├── skills.py      # Skill learning with class bonuses
│   ├── inventory.py   # Item management
│   ├── shop.py        # Commerce transactions
│   ├── bank.py        # Account management
│   ├── quest_log.py   # Quest tracking
│   └── achievements.py
├── systems/           # Cross-cutting systems
│   └── combat.py      # Combat resolution
└── game/              # Game loop and state management
    └── game_state.py  # Save/load and game state

scripts/
├── play_game.py       # Main game entry point (playable CLI RPG)
└── run_demo.py        # Feature demonstration

docs/
├── README.md          # Detailed documentation
├── copilot-instructions.md  # Development guidelines
└── DOCTEST_IMPLEMENTATION.md
```

## Running

```powershell
# Play the game (main CLI RPG)
C:/Users/Alexa/AppData/Local/Programs/Python/Python313/python.exe scripts\play_game.py

# Run feature demo
C:/Users/Alexa/AppData/Local/Programs/Python/Python313/python.exe scripts\run_demo.py

# Run all tests (pytest + doctests)
powershell -ExecutionPolicy Bypass -File .\scripts\run_all_tests.ps1

# Run only pytest
C:/Users/Alexa/AppData/Local/Programs/Python/Python313/python.exe -m pytest
```

## Test Coverage

✅ **51 passing tests** (including doctests)
- Character classes and stat modifiers
- Skill learning with class preferences
- Universal skills with categories
- Quest system with objectives
- Achievement tracking
- Combat, inventory, shop, bank systems

## Development Principles

- **Red-Green-Refactor** - Write failing test first, implement minimal code, refactor
- **Domain-Driven Design** - Entities separate from services, clear separation of concerns
- **Dependency Injection** - Protocol-based injection for testability (e.g., RandomProvider)
- **Semantic Naming** - Verbose, intention-revealing names following best practices
- **Co-located Tests** - Tests live next to source code (*_test.py pattern)
- **Flexible Specialization** - Classes provide bonuses without hard restrictions

## Documentation

See `docs/copilot-instructions.md` for comprehensive development guidelines including:
- TDD workflow and testing conventions
- Architecture patterns and design principles
- Code style and naming conventions
- Common pitfalls to avoid

## License

Educational project demonstrating TDD and clean architecture principles.
