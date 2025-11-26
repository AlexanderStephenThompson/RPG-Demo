import pytest

from rpg.entities.character import Character


def test_character_creation():
    c = Character(name="Alice", max_hp=30, attack=5, defense=2)
    assert c.name == "Alice"
    assert c.max_hp == 30
    assert c.hp == 30
    assert c.attack == 5
    assert c.defense == 2
    assert c.is_alive()


def test_take_damage_and_death():
    c = Character("Bob", max_hp=10, attack=2, defense=0)
    c.take_damage(4)
    assert c.hp == 6
    c.take_damage(10)
    assert c.hp == 0
    assert not c.is_alive()


def test_invalid_values():
    with pytest.raises(ValueError):
        Character("X", max_hp=0)
    c = Character("Y", max_hp=5)
    with pytest.raises(ValueError):
        c.take_damage(-1)
    with pytest.raises(ValueError):
        c.heal(-5)


def test_currency_tracking():
    character = Character("Merchant", max_hp=20)
    assert character.currency == 0
    character.add_currency(50)
    assert character.currency == 50
    character.add_currency(25)
    assert character.currency == 75


def test_remove_currency():
    character = Character("Merchant", max_hp=20)
    character.add_currency(100)
    result = character.remove_currency(30)
    assert result is True
    assert character.currency == 70


def test_remove_currency_insufficient_funds():
    character = Character("Poor", max_hp=20)
    character.add_currency(10)
    result = character.remove_currency(50)
    assert result is False
    assert character.currency == 10


def test_currency_validation():
    character = Character("Rich", max_hp=20)
    with pytest.raises(ValueError):
        character.add_currency(-10)
    with pytest.raises(ValueError):
        character.remove_currency(-5)
