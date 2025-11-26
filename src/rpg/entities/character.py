from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Character:
    """Represents a game character with health, combat stats, and state.

    Pure domain entity - contains only character data and validation.
    Does not manage inventory (delegated to InventoryService).

    Attributes:
        name: Character's display name
        max_hp: Maximum hit points (must be positive)
        attack: Attack stat used in damage calculation
        defense: Defense stat that reduces incoming damage
        hp: Current hit points (auto-initialized to max_hp)
        currency: Amount of money in dollars (auto-initialized to 0)
    """

    name: str
    max_hp: int
    attack: int = 0
    defense: int = 0

    def __post_init__(self) -> None:
        if self.max_hp <= 0:
            raise ValueError("max_hp must be positive")
        self.hp: int = int(self.max_hp)
        self.currency: int = 0

    def is_alive(self) -> bool:
        """Return True if character has HP remaining, False otherwise."""
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        """Reduce character's HP by the given amount.

        HP is clamped to minimum 0. Character dies (hp=0) if damage exceeds current hp.

        Args:
            amount: Non-negative damage to apply

        Raises:
            ValueError: If amount is negative

        Examples:
            >>> character = Character("Hero", max_hp=50)
            >>> character.take_damage(15)
            >>> character.hp
            35
            >>> character.take_damage(100)  # Exceeds remaining HP
            >>> character.hp  # Clamped to 0
            0
            >>> character.is_alive()
            False
        """
        if amount < 0:
            raise ValueError("damage amount must be non-negative")
        self.hp = max(0, self.hp - int(amount))

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
        if amount < 0:
            raise ValueError("heal amount must be non-negative")
        self.hp = min(self.max_hp, self.hp + int(amount))

    def add_currency(self, amount: int) -> None:
        """Add currency (dollars) to the character's wallet.

        Args:
            amount: Non-negative dollar amount to add

        Raises:
            ValueError: If amount is negative

        Examples:
            >>> character = Character("Merchant", max_hp=20)
            >>> character.currency
            0
            >>> character.add_currency(50)
            >>> character.currency
            50
            >>> character.add_currency(25)
            >>> character.currency
            75
        """
        if amount < 0:
            raise ValueError("currency amount must be non-negative")
        self.currency += int(amount)

    def remove_currency(self, amount: int) -> bool:
        """Remove currency (dollars) from the character's wallet.

        Only removes currency if character has sufficient funds. Does not allow negative balance.

        Args:
            amount: Non-negative dollar amount to remove

        Returns:
            True if currency was removed, False if insufficient funds

        Raises:
            ValueError: If amount is negative

        Examples:
            >>> character = Character("Rich", max_hp=20)
            >>> character.add_currency(100)
            >>> character.remove_currency(30)
            True
            >>> character.currency
            70
            >>> character.remove_currency(200)  # Insufficient funds
            False
            >>> character.currency  # Unchanged
            70
        """
        if amount < 0:
            raise ValueError("currency amount must be non-negative")
        if self.currency >= amount:
            self.currency -= int(amount)
            return True
        return False
