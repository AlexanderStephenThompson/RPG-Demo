from rpg.entities.character import Character
from rpg.entities.character_class import CharacterClass
from rpg.entities.predefined_classes import WARRIOR, MAGE, ROGUE


def test_warrior_class_modifies_base_stats():
    # Warrior gets 1.5x HP and +2 attack
    warrior = Character("Conan", max_hp=100, attack=5, defense=2, character_class=WARRIOR)
    
    # HP should be multiplied by 1.5
    assert warrior.max_hp == 150
    assert warrior.hp == 150
    
    # Attack should have +2 bonus
    assert warrior.attack == 7  # 5 base + 2 bonus
    
    # Defense unchanged (no bonus)
    assert warrior.defense == 2


def test_mage_class_modifies_base_stats():
    # Mage gets 0.8x HP and -1 defense
    mage = Character("Merlin", max_hp=100, attack=3, defense=2, character_class=MAGE)
    
    # HP should be multiplied by 0.8
    assert mage.max_hp == 80
    assert mage.hp == 80
    
    # Attack unchanged (no bonus)
    assert mage.attack == 3
    
    # Defense should have -1 penalty
    assert mage.defense == 1  # 2 base - 1 penalty


def test_rogue_class_balanced_stats():
    # Rogue has balanced modifiers
    rogue = Character("Shadow", max_hp=100, attack=5, defense=2, character_class=ROGUE)
    
    # HP multiplier is 1.0 (no change)
    assert rogue.max_hp == 100
    assert rogue.hp == 100
    
    # Attack gets +1 bonus
    assert rogue.attack == 6  # 5 base + 1 bonus
    
    # Defense gets +1 bonus
    assert rogue.defense == 3  # 2 base + 1 bonus


def test_character_without_class_uses_defaults():
    # Character without class should use base stats
    classless = Character("Generic", max_hp=50, attack=3, defense=1)
    
    assert classless.max_hp == 50
    assert classless.hp == 50
    assert classless.attack == 3
    assert classless.defense == 1


def test_class_validation():
    from pytest import raises
    
    # Empty ID
    with raises(ValueError):
        CharacterClass(id="", name="Bad", description="Test")
    
    # Empty name
    with raises(ValueError):
        CharacterClass(id="bad", name="", description="Test")
    
    # Invalid HP multiplier
    with raises(ValueError):
        CharacterClass(id="bad", name="Bad", description="Test", hp_multiplier=0)
    
    with raises(ValueError):
        CharacterClass(id="bad", name="Bad", description="Test", hp_multiplier=-1)
