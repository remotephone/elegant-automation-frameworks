from pytest import mark


@mark.skip
@mark.parametrize("tv_brand", [("Samsung"), ("Sony"), ("Vizio")])
def test_television_turns_on(tv_brand):
    # This is a toy example to show we're going through different TVs
    print(f"{tv_brand} turns on as expected")


def test_television_turns_on(tv_brand):
    # This is a toy example to show we're going through different TVs
    print(f"{tv_brand} turns on as expected")


@mark.skip
def test_browser_can_get_to_training_ground(browser):
    browser.get("http://techstepacademy.com/training-ground")
