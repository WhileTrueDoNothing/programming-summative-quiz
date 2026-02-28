from quiz_utils import QuestionGenerator
from quiz_utils import Question
import pytest
import pandas as pd

@pytest.fixture
def ez_maths_df():
    ez_maths_dict = {
        "problem": [
            "2 x 6",
            "3 x 4",
            "5 squared",
            "35 - 23",
            "99 / 9",
            "the square root of 144",
            "the square root of 144"
        ],
        "solution": ["12", "12", "25", "12", "11", "12", "-12"]
    }
    return pd.DataFrame(ez_maths_dict)


@pytest.fixture
def ez_maths_q_generator(ez_maths_df):
    return QuestionGenerator(
        q_details=(
            ("What is {problem}?", "solution"),
            ("What would you calculate to get {solution}?", "problem")
        ),
        q_data=ez_maths_df,
    )

@pytest.fixture
def ez_maths_q(ez_maths_q_generator):
    ez_maths_q = ez_maths_q_generator.gen_q_from_row(row_id = 5, q_details = ez_maths_q_generator.get_q_details()[0])
    return ez_maths_q

def test_q_generator_data_cols(ez_maths_q_generator):
    ez_maths_cols = ez_maths_q_generator.get_q_data().columns.tolist()
    assert ez_maths_cols == ["problem", "solution", "row_used"]


def test_get_colnames_from_text(ez_maths_q_generator):
    assert ez_maths_q_generator.get_colnames_from_text(ez_maths_q_generator.get_q_details()[0][0]) == ["problem"]

def test_mark_row_as_used(ez_maths_q_generator):
    index_to_test = 3
    ez_maths_q_generator.mark_row_as_used(index_to_test)
    assert ez_maths_q_generator.get_q_data().loc[index_to_test, "row_used"]

def test_q_from_row(ez_maths_q):
    assert ez_maths_q.get_all_answers() == ["12","-12"]
    assert ez_maths_q.get_q_text() == "What is the square root of 144?"
    assert ez_maths_q.check_answer("12")
    assert not ez_maths_q.check_answer("-12")

def test_random_q_gen(ez_maths_q_generator):
    random_q = ez_maths_q_generator.gen_random_q()
    assert isinstance(random_q, Question)
    assert random_q.check_answer(random_q.get_valid_answers()[0])

def test_gen_multiple_random_q(ez_maths_q_generator):
    q_list = []
    for i in range(0,7):
        q_list.append(ez_maths_q_generator.gen_random_q())
    with pytest.raises(ValueError):
        ez_maths_q_generator.gen_random_q()

def test_gen_alt_options(ez_maths_q_generator, ez_maths_q):
    ez_alt_options = ez_maths_q_generator.gen_alt_options(q_to_gen_for=ez_maths_q, total_q_optns=3)
    assert set(ez_alt_options) == {"25","11"}

def test_gen_alt_options_error(ez_maths_q_generator, ez_maths_q):
    with pytest.raises(ValueError):
        ez_maths_q_generator.gen_alt_options(q_to_gen_for=ez_maths_q, total_q_optns=4)

def test_reset_use_rows(ez_maths_q_generator):
    for i in range(0,7):
        ez_maths_q_generator.mark_row_as_used(i)
    ez_maths_q_generator.reset_used_rows()
    q_data = ez_maths_q_generator.get_q_data()
    num_unused_rows = q_data.loc[q_data["row_used"], "row_used"].size
    assert num_unused_rows == 0