# TDD Python RPG - AI Agent Instructions

## Project Philosophy: Strict TDD & Design Patterns

This is a **Test-Driven Development** RPG built with explicit design patterns. Always follow the Red-Green-Refactor cycle:
1. Write a failing test first (RED)
2. Write minimal code to pass the test (GREEN)
3. Refactor while keeping tests green

**Critical**: Never implement game logic without a corresponding test. Tests are written before implementation code.

**⚠️ CRITICAL: ALL CODE REQUIRES TESTS - NO EXCEPTIONS**

This includes:
- ✅ Core entities and services (obvious)
- ✅ Integration/coordination layers (GameState, service orchestration)
- ✅ Interface code of ANY kind:
  - CLI (game loops, menus, console commands)
  - Web (routes, handlers, controllers)
  - API (endpoints, request processing)
  - GUI (event handlers, callbacks)
  - Scripts (automation, utilities)
- ✅ "Glue code" and adapters between layers
- ✅ Save/load and persistence logic
- ✅ Configuration and initialization code
- ✅ LITERALLY ANY CODE THAT EXECUTES

**Common failure mode**: "This is just simple interface/integration code, I don't need tests."

**Reality**: Interface and integration code has the HIGHEST bug density because:
- It calls methods that may not exist (wrong API assumptions)
- It makes typos in method names that compilers don't catch
- It assumes API contracts that are incorrect
- It has flow edge cases and error conditions you didn't consider
- It coordinates multiple services with incorrect ordering or state

**Real examples from this project:**
- Called `xp_for_next_level()` when method is `next_threshold()`
- Called `has_item()` when InventoryService doesn't have this method
- These bugs existed in ~500 lines of untested interface code
- TDD would have caught both in under 30 seconds

**If you skip tests, you will ship bugs. Period.**

Write the test FIRST. Even for "trivial" code. Especially for "trivial" code.
The test is what tells you if the API you're calling actually exists.

## Architecture & Structure

### Layer Separation (Domain-Driven Design + Clean Architecture)

The project is organized by domain concepts with co-located tests:

- **`src/rpg/entities/`** - Pure domain entities (data models with validation only)
  - `character.py` - Character entity with HP, stats, currency
  - `character_test.py` - Character tests (co-located)
  - `item.py` - Item entity with equipment/consumable properties
  - `item_test.py` - Item tests (co-located)
  - No dependencies on services or systems - purely data and validation
  
- **`src/rpg/services/`** - Business logic and domain services
  - `inventory.py` - InventoryService manages items, equip/unequip logic
  - `inventory_test.py` - Inventory tests (co-located)
  - `shop.py` - ShopService handles commerce transactions
  - `shop_test.py` - Shop tests (co-located)
  - `bank.py` - BankService manages account balances and transfers
  - `bank_test.py` - Bank tests (co-located)
  - Services coordinate between entities and apply business rules
  
- **`src/rpg/systems/`** - Cross-cutting game systems
  - `combat.py` - Combat resolution with damage calculation
  - `combat_test.py` - Combat tests (co-located)
  - Systems operate on entities but don't belong to a single service

- **`scripts/`** - Runnable demo and utility scripts
  - `run_demo.py` - Interactive demo showcasing all systems

- **`docs/`** - All documentation
  - `README.md` - Project overview
  - `copilot-instructions.md` - Development guidelines

**Benefits of this structure:**
- ✅ No circular dependencies (entities don't import services)
- ✅ Clear separation of data (entities) vs behavior (services)
- ✅ Intuitive navigation - related concepts grouped together
- ✅ Easy to extend - add new entities/services without restructuring
- ✅ Src layout - Prevents accidental imports, forces explicit package installation
- ✅ Co-located tests - Tests live next to the code they verify for easy access

### Dependency Injection Pattern (Critical)

Non-deterministic behavior (randomness, time, I/O) is **always injected** via Protocol interfaces:

```python
# CORRECT: Testable with injected RNG
from typing import Protocol

class RandomProvider(Protocol):
    def random(self) -> float: ...

def resolve_attack(attacker, defender, random_provider: RandomProvider | None = None):
    # random_provider is injected, making tests deterministic
```

See `src/rpg/systems/combat.py` and `src/rpg/systems/combat_test.py::_FixedRng` for the canonical example.

### Stat Modification Pattern

Equipment/buffs modify `Character` stats **directly** via reversible operations:

```python
# Equip adds to stats (src/rpg/services/inventory.py::InventoryService.equip)
character.attack += item.equip_attack

# Unequip subtracts exactly the same amount
character.attack -= item.equip_attack
```

Tests verify these operations are symmetric (see `src/rpg/services/inventory_test.py::test_equip_and_unequip_changes_stats`).

## Testing Conventions

### Test Structure & Co-located Tests
- **Co-located test files**: Tests live next to the code they verify using `*_test.py` naming
  - `src/rpg/entities/character.py` → `src/rpg/entities/character_test.py`
  - `src/rpg/services/shop.py` → `src/rpg/services/shop_test.py`
- **Benefits**: Easy to find tests, less context switching, tests don't fall out of sync
- **Descriptive test names**: `test_take_damage_and_death()`, not `test_damage()`
- **Arrange-Act-Assert** pattern in every test

### Doctests: Executable Documentation
- **Purpose**: Simple, illustrative examples in docstrings that double as tests
- **Use for**: Showing API usage, demonstrating basic scenarios, living documentation
- **Don't use for**: Complex test logic, edge cases, tests requiring fixtures/mocks
- **Format**: Use `>>>` prompts in `Examples:` section of docstrings
- **Example**:
  ```python
  def heal(self, amount: int) -> None:
      """Restore character's HP by the given amount.
      
      HP is clamped to max_hp. Cannot exceed maximum health.
      
      Args:
          amount: Non-negative healing to apply
          
      Raises:
          ValueError: If amount is negative
          
      Examples:
          >>> character = Character("Hero", max_hp=50)
          >>> character.take_damage(30)  # hp = 20
          >>> character.heal(15)
          >>> character.hp
          35
          >>> character.heal(100)  # Exceeds max_hp
          >>> character.hp  # Clamped to max_hp
          50
      """
  ```
- **Running doctests**: Use `powershell -ExecutionPolicy Bypass -File .\scripts\run_all_tests.ps1` to run both pytest and doctests

### Pytest: Comprehensive Testing
- **Purpose**: Full test coverage including edge cases, error conditions, complex scenarios
- **Use for**: Testing business logic, validating error handling, integration tests, stateful operations
- **Test doubles**: Create inline test doubles (e.g., `_FixedRng` for deterministic randomness)

### Running Tests (Windows/PowerShell)

```powershell
# Run ALL tests (pytest + doctests)
powershell -ExecutionPolicy Bypass -File .\scripts\run_all_tests.ps1

# Run only pytest tests
.\.venv\Scripts\python.exe -m pytest

# Run specific test file
.\.venv\Scripts\python.exe -m pytest src/rpg/entities/character_test.py

# Run with verbose output
.\.venv\Scripts\python.exe -m pytest -v

# Stop on first failure (useful during TDD)
.\.venv\Scripts\python.exe -m pytest --maxfail=1

# Run doctests manually for a single file
.\.venv\Scripts\python.exe -m doctest src/rpg/entities/character.py -v
```

**Note**: The main test runner (`.\scripts\run_all_tests.ps1`) runs pytest first (26 tests), then doctests (6 modules) for comprehensive coverage.

### Test Doubles for Dependencies

Create lightweight test doubles inline (not external mocking frameworks unless necessary):

```python
# Preferred: Inline test double (see tests/systems/test_combat.py)
class _FixedRng:
    def __init__(self, value: float):
        self._value = value
    def random(self) -> float:
        return self._value

# Use in test
random_provider = _FixedRng(0.1)  # Deterministic random value
```

## Code Style & Patterns

### Type Hints
- **All public functions/methods** have full type hints (params + return)
- Use `from __future__ import annotations` for forward references
- Protocols use `@runtime_checkable` when runtime type checking is needed

### Dataclasses for Domain Models
- Prefer `@dataclass` for entities: `Character`, `Item`
- Use `__post_init__` for validation and computed attributes
- Example: `Character.__post_init__` initializes `self.hp` from `max_hp`

### Error Handling
- Raise `ValueError` for invalid domain operations (negative damage, invalid stats)
- Tests verify exceptions with `pytest.raises(ValueError)`

### Docstrings
- **All public functions/classes** must have docstrings
- Use concise, complete one-liners for simple functions; multi-line for complex behavior
- Include parameter descriptions, return values, and side effects explicitly
- **Format**: Use Google-style docstrings for consistency
- **Example (simple)**:
  ```python
  def is_alive(self) -> bool:
      """Return True if character has HP remaining, False otherwise."""
  ```
- **Example (complex)**:
  ```python
  def resolve_attack(attacker: Character, defender: Character, 
                     random_provider: RandomProvider | None = None, 
                     crit_chance: float = 0.0) -> int:
      """Resolve a single attack from attacker to defender.
      
      Calculates damage as (attacker.attack - defender.defense), minimum 0.
      If random_provider is provided and random roll < crit_chance, damage is doubled.
      Applies damage directly to defender's HP.
      
      Args:
          attacker: Character performing the attack
          defender: Character receiving damage (modified in-place)
          random_provider: Optional RNG for critical hit calculation
          crit_chance: Probability of critical hit (0.0-1.0), requires random_provider
          
      Returns:
          The final damage value applied to defender
          
      Examples:
          Basic attack without crits:
          >>> hero = Character("Hero", max_hp=50, attack=10)
          >>> enemy = Character("Goblin", max_hp=20, defense=3)
          >>> damage = resolve_attack(hero, enemy)
          >>> # damage = 10 - 3 = 7, enemy.hp = 13
          
          Attack with deterministic crit for testing:
          >>> rng = _FixedRng(0.1)  # Always returns 0.1
          >>> damage = resolve_attack(hero, enemy, random_provider=rng, crit_chance=0.5)
          >>> # 0.1 < 0.5, so crit occurs: damage = (10-3) * 2 = 14
      """
  ```
- **For complex classes/functions**: Add `Examples:` section showing typical usage patterns
- **Leave no ambiguity**: Readers should know inputs, outputs, side effects, and edge cases without reading implementation

### Naming Conventions
- **Prefer verbose, semantic names over abbreviations**: Use `character`, `attacker`, `defender` instead of `char`, `atk`, `def`
- Variable names should be self-documenting: `critical_hit_chance` not `crit_pct`
- Avoid single-letter variables except for simple loops or well-understood math (e.g., `x`, `y` for coordinates)
- Example: `max_hp` and `heal_amount` are clear; avoid `mhp`, `amt`

#### Method Naming & API Design
Method names are a **social contract** - they should clearly communicate who is acting, what they're doing, and to whom/what. Follow these principles:

1. **Avoid directional ambiguity**: The method name should match the perspective of the object it's called on
   - ❌ `shop.buy_item(item_id, buyer)` - Confusing! "buy" implies shop is buyer
   - ✅ `shop.sell_item_to(item_id, buyer)` - Clear! Shop is seller, item goes to buyer
   - ✅ `shop.sell(item_id, to=buyer)` - Also clear with named parameter

2. **Use prepositions to clarify direction**: `to`, `from`, `into`, `onto` make data flow explicit
   - `transfer_money_to(account)` - Money flows TO the account
   - `remove_item_from(inventory)` - Item comes FROM the inventory
   - `add_buff_to(character)` - Buff is applied TO the character

3. **Named parameters for semantic clarity**: When a parameter's role isn't obvious, use keyword arguments
   ```python
   # Without named parameter - unclear
   shop.sell("potion1", character)
   
   # With named parameter - crystal clear
   shop.sell("potion1", to=character)
   ```

4. **Avoid overly abstract verbs**: "process", "handle", "manage" are vague
   - ❌ `shop.process_purchase(item_id, buyer)` - What kind of processing?
   - ✅ `shop.sell_item_to(item_id, buyer)` - Specific business operation

5. **Read method calls aloud**: If it sounds grammatically wrong, rename it
   - "The shop buys item to character" ❌
   - "The shop sells item to character" ✅

### Imports
- Standard library first, then third-party, then local imports
- Use relative imports within package: `from rpg.core.character import Character`

## Development Workflow

### Adding a New Feature (TDD Cycle)

1. **Write the test first** (it will fail):
   ```powershell
   # Create tests/test_newfeature.py
   # Run to verify RED
   python -m pytest tests/test_newfeature.py
   ```

2. **Implement minimal code** in `rpg/core/newfeature.py`

3. **Run tests to verify GREEN**:
   ```powershell
   python -m pytest tests/test_newfeature.py
   ```

4. **Refactor** while keeping tests green

5. **Run full suite** before committing:
   ```powershell
   python -m pytest
   ```

### Planned Design Patterns (Not Yet Implemented)

When these features are added, use these patterns:
- **Event Bus** (Observer): Combat/item effects emit events → logging/UI subscribers react
- **Command Pattern**: Player actions as command objects (enables undo/redo)
- **Repository**: Abstract persistence (in-memory for tests, JSON for demo)
- **Strategy**: Swap damage formulas, AI behaviors

## Common Pitfalls to Avoid

1. **Don't mutate Character stats without symmetry**: If you add a buff, ensure there's a way to remove it exactly
2. **Don't use global state or singletons**: Always inject dependencies via constructors/parameters
3. **Don't skip writing tests**: If you find yourself implementing logic first, stop and write the test
4. **Don't use `random.random()` directly**: Inject a `RandomProvider` protocol so tests can control outcomes

## File/Module Naming

- Modules: `snake_case.py` (e.g., `combat.py`, `game_service.py`)
- Classes: `PascalCase` (e.g., `Character`, `RandomProvider`)
- Functions/methods: `snake_case` (e.g., `resolve_attack`, `is_alive`)
- Test functions: `test_<behavior>` (e.g., `test_critical_hit_doubles_damage_with_rng`)

## Key Files to Reference

- **`src/rpg/systems/combat.py`** - Example of Protocol-based DI
- **`src/rpg/services/inventory.py`** - Example of stat modification pattern
- **`tests/systems/test_combat.py`** - Example of test doubles (`_FixedRng`)
- **`tests/entities/test_character.py`** - Example of dataclass validation tests
- **`pytest.ini`** - Test runner configuration (includes pythonpath = src)
- **`pyproject.toml`** - Package configuration with src layout
