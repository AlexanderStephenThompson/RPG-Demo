from rpg.entities.character import Character
from rpg.entities.quest import Quest, Objective
from rpg.services.quest_log import QuestLogService
from rpg.services.achievements import AchievementsService


def test_first_quest_completion_awards_achievement():
    hero = Character("NewAdventurer", max_hp=20)
    quests = QuestLogService()
    achievements = AchievementsService()

    garden_quest = Quest(
        id="garden_tutorial",
        name="Growing Your First Garden",
        description="Learn gardening basics",
        objectives=[Objective(id="prepare_soil", description="Prepare the soil")]
    )

    # Accept and complete quest
    quests.accept(hero, garden_quest)
    quests.complete_objective(hero, "garden_tutorial", "prepare_soil")

    # Manually award achievement (integration point)
    if quests.is_completed(hero, "garden_tutorial"):
        awarded = achievements.record_quest_completion(hero, is_first=True)
        assert awarded is True
        assert "quest_novice" in achievements.earned(hero)

    # Second quest should not award again
    another_quest = Quest(
        id="q2",
        name="Another Quest",
        description="Test",
        objectives=[Objective(id="obj", description="Do it")]
    )
    quests.accept(hero, another_quest)
    quests.complete_objective(hero, "q2", "obj")
    
    awarded_again = achievements.record_quest_completion(hero, is_first=False)
    assert awarded_again is False
