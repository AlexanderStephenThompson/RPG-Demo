from rpg.entities.character import Character
from rpg.entities.quest import Quest, Objective
from rpg.services.quest_log import QuestLogService


def test_accept_and_complete_single_objective_quest():
    hero = Character("Gardener", max_hp=20)
    log = QuestLogService()

    quest = Quest(
        id="garden_tutorial",
        name="Growing Your First Garden",
        description="Learn the basics of gardening",
        objectives=[Objective(id="prepare_soil", description="Prepare the soil")]
    )

    # Initially no quests
    assert log.active(hero) == []
    assert log.completed(hero) == []

    # Accept quest
    assert log.accept(hero, quest) is True
    assert log.active(hero) == ["garden_tutorial"]
    assert log.is_completed(hero, "garden_tutorial") is False

    # Complete the objective
    assert log.complete_objective(hero, "garden_tutorial", "prepare_soil") is True
    assert log.is_completed(hero, "garden_tutorial") is True

    # Quest moves to completed
    assert log.active(hero) == []
    assert log.completed(hero) == ["garden_tutorial"]


def test_cannot_accept_same_quest_twice():
    hero = Character("Farmer", max_hp=20)
    log = QuestLogService()

    quest = Quest(
        id="q1",
        name="Test Quest",
        description="Test",
        objectives=[Objective(id="o1", description="Do something")]
    )

    assert log.accept(hero, quest) is True
    assert log.accept(hero, quest) is False  # Duplicate
    assert log.active(hero) == ["q1"]


def test_multi_objective_quest_completion():
    hero = Character("Student", max_hp=20)
    log = QuestLogService()

    quest = Quest(
        id="garden_full",
        name="Complete Garden Setup",
        description="Set up your garden",
        objectives=[
            Objective(id="prepare_soil", description="Prepare soil"),
            Objective(id="plant_seeds", description="Plant seeds"),
            Objective(id="water_garden", description="Water the garden")
        ]
    )

    log.accept(hero, quest)
    assert log.is_completed(hero, "garden_full") is False

    # Complete first two objectives
    log.complete_objective(hero, "garden_full", "prepare_soil")
    log.complete_objective(hero, "garden_full", "plant_seeds")
    assert log.is_completed(hero, "garden_full") is False  # Not done yet

    # Complete final objective
    log.complete_objective(hero, "garden_full", "water_garden")
    assert log.is_completed(hero, "garden_full") is True
    assert log.completed(hero) == ["garden_full"]


def test_completing_invalid_objective_returns_false():
    hero = Character("Adventurer", max_hp=20)
    log = QuestLogService()

    quest = Quest(
        id="q1",
        name="Quest",
        description="Desc",
        objectives=[Objective(id="obj1", description="Do it")]
    )

    log.accept(hero, quest)

    # Invalid objective ID
    assert log.complete_objective(hero, "q1", "nonexistent") is False

    # Invalid quest ID
    assert log.complete_objective(hero, "invalid_quest", "obj1") is False
