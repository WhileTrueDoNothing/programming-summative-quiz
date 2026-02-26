from quiz_utils import Question
import pytest


def test_smoke():
    assert 2 + 2 == 4

@pytest.fixture
def test_q():
    test_q = Question(q_text = "What's the full name for the postcode area MK?", answer="Milton Keynes", a_col="postcode_area_name")
    return test_q

def test_q_answer_correct(test_q):
    assert test_q.check_answer("Milton Keynes")

def test_q_answer_incorrect(test_q):
    assert not test_q.check_answer("Miton Keynes")