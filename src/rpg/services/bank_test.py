import pytest

from rpg.entities.character import Character
from rpg.services.bank import BankService


def test_bank_creation():
    bank = BankService(name="First National")
    assert bank.name == "First National"


def test_deposit_from_character():
    bank = BankService(name="Vault")
    character = Character("Saver", max_hp=50)
    character.add_currency(100)

    result = bank.deposit_from(character, amount=50)
    assert result is True
    assert character.currency == 50
    assert bank.check_balance(character) == 50


def test_deposit_from_character_insufficient_funds():
    bank = BankService(name="Vault")
    character = Character("Poor", max_hp=50)
    character.add_currency(25)

    result = bank.deposit_from(character, amount=100)
    assert result is False
    assert character.currency == 25
    assert bank.check_balance(character) == 0


def test_withdraw_to_character():
    bank = BankService(name="Vault")
    character = Character("Spender", max_hp=50)
    character.add_currency(100)
    bank.deposit_from(character, amount=100)

    result = bank.withdraw_to(character, amount=50)
    assert result is True
    assert character.currency == 50
    assert bank.check_balance(character) == 50


def test_withdraw_to_character_insufficient_balance():
    bank = BankService(name="Vault")
    character = Character("Broke", max_hp=50)

    result = bank.withdraw_to(character, amount=100)
    assert result is False
    assert character.currency == 0
    assert bank.check_balance(character) == 0


def test_check_balance_no_account():
    bank = BankService(name="Vault")
    character = Character("Stranger", max_hp=50)

    assert bank.check_balance(character) == 0


def test_transfer_between_characters():
    bank = BankService(name="Vault")
    sender = Character("Rich", max_hp=50)
    receiver = Character("Friend", max_hp=50)

    sender.add_currency(200)
    bank.deposit_from(sender, amount=200)

    result = bank.transfer_between(sender, receiver, amount=100)
    assert result is True
    assert bank.check_balance(sender) == 100
    assert bank.check_balance(receiver) == 100


def test_transfer_between_insufficient_balance():
    bank = BankService(name="Vault")
    sender = Character("Poor Sender", max_hp=50)
    receiver = Character("Hopeful", max_hp=50)

    sender.add_currency(50)
    bank.deposit_from(sender, amount=50)

    result = bank.transfer_between(sender, receiver, amount=100)
    assert result is False
    assert bank.check_balance(sender) == 50
    assert bank.check_balance(receiver) == 0
