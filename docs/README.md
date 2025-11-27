# TDD Python RPG

A Python RPG built strictly following Test-Driven Development and design patterns. Features clean architecture with domain-driven design for maximum clarity and maintainability.

## Project Structure

```
demo/
├── src/rpg/           # All source code with co-located tests
│   ├── entities/      # Pure domain models
│   │   ├── character.py
│   │   ├── character_test.py
│   │   ├── item.py
│   │   └── item_test.py
│   ├── services/      # Business logic
│   │   ├── inventory.py
│   │   ├── inventory_test.py
│   │   ├── shop.py
│   │   ├── shop_test.py
│   │   ├── bank.py
│   │   └── bank_test.py
│   └── systems/       # Cross-cutting systems
│       ├── combat.py
│       └── combat_test.py
├── scripts/           # Runnable scripts
│   └── run_demo.py
├── docs/              # Documentation
│   ├── README.md
│   └── copilot-instructions.md
├── pyproject.toml     # Project configuration
├── pytest.ini         # Test configuration
└── requirements-dev.txt
```

## Features

- ⚔️ **Combat System** - Turn-based combat with critical hits
- 🎒 **Inventory Management** - Equip items to modify stats
- 🏪 **Shop System** - Buy/sell items with currency
- 🏦 **Banking** - Deposit, withdraw, transfer currency
- ✅ **26 Passing Tests** - 100% TDD workflow

## Running

```powershell
# Run tests
.\.venv\Scripts\python.exe -m pytest

# Run demo
.\.venv\Scripts\python.exe scripts\run_demo.py
```

## Development Principles

- **Red-Green-Refactor** - Write failing test first, implement minimal code, refactor
- **Domain-Driven Design** - Entities separate from services, clear separation of concerns
- **Dependency Injection** - Protocol-based injection for testability (e.g., RandomProvider)
- **Semantic Naming** - Verbose, intention-revealing names following best practices
- **Src Layout** - Clean separation preventing accidental imports

See `docs/copilot-instructions.md` for comprehensive development guidelines.
