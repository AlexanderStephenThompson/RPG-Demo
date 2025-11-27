from rpg.entities.character import Character
from rpg.entities.achievement import Achievement
from rpg.services.achievements import AchievementsService


def test_award_first_purchase_once():
    hero = Character("Buyer", max_hp=20)
    svc = AchievementsService()

    first_purchase = Achievement(
        id="first_purchase", name="First Purchase", description="Bought an item for the first time"
    )

    # Initially not earned
    assert svc.earned(hero) == set()

    # Record purchase → should award achievement
    awarded = svc.record_purchase(hero, purchase_success=True)
    assert awarded is True
    assert svc.earned(hero) == {"first_purchase"}

    # Second purchase does not award again
    awarded_again = svc.record_purchase(hero, purchase_success=True)
    assert awarded_again is False
    assert svc.earned(hero) == {"first_purchase"}


def test_no_award_on_failed_purchase():
    hero = Character("Buyer", max_hp=20)
    svc = AchievementsService()
    Achievement(id="first_purchase", name="First Purchase", description="Bought an item")  # definition only

    # Failed purchase should not award
    assert svc.record_purchase(hero, purchase_success=False) is False
    assert svc.earned(hero) == set()
