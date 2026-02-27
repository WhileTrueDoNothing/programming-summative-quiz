from quiz_utils import QuestionGenerator
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
            "the square root of 144",
        ],
        "solution": ["12", "12", "25", "12", "11", "12", "-12"],
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


def test_q_generator_data_cols(ez_maths_q_generator):
    ez_maths_cols = ez_maths_q_generator.get_q_data().columns.tolist()
    assert ez_maths_cols == ["problem", "solution", "row_used"]


def test_get_colnames_from_text(ez_maths_q_generator):
    assert ez_maths_q_generator.get_colnames_from_text(ez_maths_q_generator.get_q_details()[0][0]) == ["problem"]

def test_mark_row_as_used(ez_maths_q_generator):
    index_to_test = 3
    ez_maths_q_generator.mark_row_as_used(index_to_test)
    assert ez_maths_q_generator.get_q_data().loc[index_to_test, "row_used"]