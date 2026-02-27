from quiz_utils import Question
import pytest


def test_smoke():
    assert 2 + 2 == 4


@pytest.fixture
def test_q_single_correct():
    test_q = Question(
        q_text="What is the postcode area for London?",
        answers=["E","EC","N","NW","SE","SW","W","WC"],
        a_col="postcode_area_name"
    )
    return test_q

@pytest.fixture
def test_q_multi_correct():
    test_q = Question(
        q_text="What is the postcode area for London?",
        answers=["E","EC","N","NW","SE","SW","W","WC"],
        a_col="postcode_area_name",
        allow_multiple_correct=True
    )
    return test_q

def test_q_single_answer_correct(test_q_single_correct):
    assert test_q_single_correct.check_answer("E")


def test_q_single_answer_incorrect(test_q_single_correct):
    assert not test_q_single_correct.check_answer("EC")

def test_q_multi_answer_correct(test_q_multi_correct):
    assert test_q_multi_correct.check_answer("EC")

def test_q_multi_answer_incorrect(test_q_multi_correct):
    assert not test_q_multi_correct.check_answer("NE")