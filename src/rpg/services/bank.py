from __future__ import annotations

from rpg.entities.character import Character


class BankService:
    """Service for managing a bank where characters can store currency.

    Manages character accounts with deposits, withdrawals, and transfers.
    Each character has a separate account balance tracked by the bank.

    Attributes:
        name: Bank's display name
    """

    def __init__(self, name: str) -> None:
        """Initialize a new bank with the given name.

        Args:
            name: Bank's display name
        """
        self.name = name
        self._accounts: dict[str, int] = {}

    def deposit_from(self, character: Character, amount: int) -> bool:
        """Accept a deposit from a character into their bank account.

        Transfers currency from character's wallet to their bank account.
        Creates account if character doesn't have one.

        Args:
            character: Character making the deposit (modified in-place if successful)
            amount: Currency amount to deposit

        Returns:
            True if deposit successful, False if character has insufficient funds

        Examples:
            >>> bank = BankService("Vault")
            >>> hero = Character("Hero", max_hp=50)
            >>> hero.add_currency(100)
            >>> bank.deposit_from(hero, amount=50)
            True
            >>> hero.currency
            50
            >>> bank.check_balance(hero)
            50
        """
        if not character.remove_currency(amount):
            return False

        if character.name not in self._accounts:
            self._accounts[character.name] = 0

        self._accounts[character.name] += amount
        return True

    def withdraw_to(self, character: Character, amount: int) -> bool:
        """Withdraw currency from character's account to their wallet.

        Transfers currency from bank account to character's wallet.

        Args:
            character: Character making the withdrawal (modified in-place if successful)
            amount: Currency amount to withdraw

        Returns:
            True if withdrawal successful, False if insufficient account balance

        Examples:
            >>> bank = BankService("Vault")
            >>> hero = Character("Hero", max_hp=50)
            >>> hero.add_currency(100)
            >>> bank.deposit_from(hero, amount=100)
            True
            >>> bank.withdraw_to(hero, amount=50)
            True
            >>> hero.currency
            50
            >>> bank.check_balance(hero)
            50
        """
        if character.name not in self._accounts:
            return False

        if self._accounts[character.name] < amount:
            return False

        self._accounts[character.name] -= amount
        character.add_currency(amount)
        return True

    def check_balance(self, character: Character) -> int:
        """Get the current balance of a character's account.

        Args:
            character: Character to check balance for

        Returns:
            Current account balance, or 0 if no account exists

        Examples:
            >>> bank = BankService("Vault")
            >>> hero = Character("Hero", max_hp=50)
            >>> bank.check_balance(hero)
            0
            >>> hero.add_currency(100)
            >>> bank.deposit_from(hero, amount=75)
            True
            >>> bank.check_balance(hero)
            75
        """
        return self._accounts.get(character.name, 0)

    def transfer_between(
        self, sender: Character, receiver: Character, amount: int
    ) -> bool:
        """Transfer currency between two character accounts.

        Moves currency from sender's account to receiver's account.
        Creates receiver's account if it doesn't exist.

        Args:
            sender: Character sending the currency
            receiver: Character receiving the currency
            amount: Currency amount to transfer

        Returns:
            True if transfer successful, False if sender has insufficient balance

        Examples:
            >>> bank = BankService("Vault")
            >>> alice = Character("Alice", max_hp=50)
            >>> bob = Character("Bob", max_hp=50)
            >>> alice.add_currency(200)
            >>> bank.deposit_from(alice, amount=200)
            True
            >>> bank.transfer_between(alice, bob, amount=100)
            True
            >>> bank.check_balance(alice)
            100
            >>> bank.check_balance(bob)
            100
        """
        if sender.name not in self._accounts:
            return False

        if self._accounts[sender.name] < amount:
            return False

        if receiver.name not in self._accounts:
            self._accounts[receiver.name] = 0

        self._accounts[sender.name] -= amount
        self._accounts[receiver.name] += amount
        return True
