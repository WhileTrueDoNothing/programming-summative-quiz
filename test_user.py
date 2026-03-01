from quiz_utils import User
import pytest

@pytest.fixture
def test_user():
    return User(name="Test")

def test_no_lives():
    with pytest.raises(ValueError):
        test_user_2 = User(name="Billy Nolives", lives=0)

def test_neg_lives():
    with pytest.raises(ValueError):
        test_user_3 = User(name="Negative Nancy", lives=-5)

def test_user_vars(test_user):
    assert test_user.get_name() == "Test"
    assert test_user.get_lives() == 3
    assert test_user.get_score() == 0

def test_add_score(test_user):
    test_user.add_score()
    assert test_user.get_score() == 1
    test_user.add_score(to_add = 3)
    assert test_user.get_score() == 4

def test_lose_lives(test_user):
    test_user.lose_lives()
    assert test_user.get_lives() == 2
    test_user.lose_lives(to_lose=2)
    assert test_user.get_lives() == 0
    test_user.lose_lives(5)
    assert test_user.get_lives() == 0