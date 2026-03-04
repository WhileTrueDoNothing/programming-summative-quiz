from quiz_utils import LeaderboardManager
from quiz_utils import User
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
import plotly.graph_objects as go

@pytest.fixture
def leaderboard_csv_path(tmp_path):
    score_data = pd.DataFrame({"user":["Victor","Casey","Tony","Adrian","Yumei","Mal"], "score":[11,7,3,12,15,5]})
    path_to_use = tmp_path / "test_leaderboard.csv"
    score_data.to_csv(path_to_use, index=False)
    return str(path_to_use)

@pytest.fixture
def leaderboard_mgr(leaderboard_csv_path):
    return LeaderboardManager(source_path=leaderboard_csv_path)

def test_leaderboard_data(leaderboard_mgr):
    expected_df = pd.DataFrame({"user":["Yumei","Adrian","Victor","Casey","Mal"],"score":[15,12,11,7,5]})
    assert_frame_equal(expected_df, leaderboard_mgr.get_score_data())

def test_leaderboard_fig(leaderboard_mgr):
    assert isinstance(leaderboard_mgr.get_leader_chart(), go.Figure)

def test_save_and_update(leaderboard_mgr, leaderboard_csv_path):
    user_1 = User(name="Lil",score=9)
    leaderboard_mgr.save_result_and_update(user_1)
    expected_df_1 = pd.DataFrame({"user":["Yumei","Adrian","Victor","Lil","Casey"],"score":[15,12,11,9,7]})
    assert_frame_equal(expected_df_1, leaderboard_mgr.get_score_data())
    user_2 = User(name="Mel", score=6)
    leaderboard_mgr.save_result_and_update(user_2)
    expected_df_2 = pd.DataFrame({"user":["Yumei","Adrian","Victor","Lil","Mel"],"score":[15,12,11,9,6]})
    assert_frame_equal(expected_df_2, leaderboard_mgr.get_score_data())
    full_leaderboard = pd.read_csv(leaderboard_csv_path)
    assert len(full_leaderboard.index) == 8
