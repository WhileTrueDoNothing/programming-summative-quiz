"""Tools for creating questions and quizzes."""

import random  # for picking random items from lists
import pandas as pd  # for importing and managing question data
import string  # for handling custom question strings
import plotly.graph_objects as go  # for creating the leaderboard chart
import re  # for regex matching


class Question:
    """A question that can be answered by a free text input."""

    q_text: str
    answers: list[str]
    a_col: str
    allow_multiple_correct: bool

    def __init__(
        self,
        q_text: str,
        answers: list[str],
        a_col: str,
        allow_multiple_correct: bool = False,
    ):
        """
        Create a new Question.

        Args:
            q_text (str): The text for the question to be asked.
            answers (list[str]): The correct answer(s) for the question.
            a_col (str): The column in the data the answer is from (for generating options to select from).
            allow_multiple_correct (bool, optional): Whether to display multiple correct answers.
        """
        self.q_text = q_text
        self.answers = answers
        self.a_col = a_col
        self.allow_multiple_correct = allow_multiple_correct

    def get_q_text(self):
        """Returns the question's text."""
        return self.q_text

    def get_all_answers(self):
        """Returns the list of all the Question's answers, no matter the value of allow_multiple_correct."""
        return self.answers

    def get_valid_answers(self):
        """Returns the full list of answers if allow_multiple_correct is true, returns only the first otherwise."""
        if self.allow_multiple_correct:
            return self.answers
        else:
            return self.answers[:1]

    def get_a_col(self):
        """Returns the name of the column the Question's answers are from."""
        return self.a_col

    def check_answer(self, a_to_check: str):
        """
        Checks a given input against a list of the Question's answer(s).
        Returns True if the input is present, False otherwise.
        """
        valid_answers = self.get_valid_answers()

        if a_to_check.lower() in [answer.lower() for answer in valid_answers]:
            return True
        else:
            return False


class QuestionGenerator:
    """Manages a pandas DataFrame and uses it to generate Question objects."""

    q_details: tuple[tuple[str, str]]
    q_data: pd.DataFrame

    def __init__(
        self,
        q_details: tuple[tuple[str, str]],
        q_data: pd.DataFrame = None,
        q_data_source_path: str = None,
    ):
        """
        Creates a new QuestionGenerator.

        Args:
            q_details (tuple[tuple[str,str]]): Question details. The first item in the tuple should be a formattable
                string for the question text, with column names in {} where their value should be. Second value is
                the name of the column to get the answer from.
            q_data (pandas.DataFrame, optional*): A DataFrame to generate questions from. Defaults to None.
                Must be provided if q_data_source_path is None.
            q_data_source_path (str, optional*): The path to a CSV file containing question data. Defaults to None.
                Must be provided if q_data is None.

        Raises:
            TypeError: If no question data is provided.
        """

        self.q_details = q_details

        if q_data is not None:
            self.q_data = q_data
        elif q_data_source_path is not None:
            self.q_data = pd.read_csv(q_data_source_path, index_col=None)
        else:
            raise TypeError(
                "No question data was provided. Please provide either a DataFrame or a path to a CSV file."
            )

        self.q_data["row_used"] = False

    def get_q_details(self):
        """Returns the QuestionGenerator's q_details tuple tuple."""
        return self.q_details

    def get_q_data(self):
        """Returns the QuestionGenerator's q_data DataFrame."""
        return self.q_data

    def get_colnames_from_text(self, text: str):
        """Extracts column names from {curly brackets} in a string and returns them as a list."""
        colname_list = [
            span[1] for span in string.Formatter().parse(text) if span[1] is not None
        ]
        return list(set(colname_list))

    def mark_row_as_used(self, row_id: int):
        """Sets the value of row_used for a given row_id to True."""
        self.q_data.loc[row_id, "row_used"] = True

    def gen_q_from_row(
        self,
        row_id: int,
        q_details: tuple[str, str],
        allow_multiple_correct: bool = False,
    ):
        """
        Generates a Question from the specified row and details.

        Args:
            row_id (int): The index of the row to create a question from.
            q_details (tuple[str,str]): The question text and answer column to be used for the question.
            allow_multiple_correct (bool, optional): Whether to display multiple correct answers. Defaults to False.

        Returns:
            Question: A Question object with the q_text, answers, a_col and allow_multiple_correct attributes
            determined by the inputs provided.
        """
        row_dict = self.q_data.loc[row_id].to_dict()

        # extract q col names from the question text
        q_cols = self.get_colnames_from_text(q_details[0])
        # get q col values from the row dict
        q_col_vals = {col: row_dict[col] for col in q_cols}
        q_text = q_details[0].format(**q_col_vals)
        # get initial answer col value from the answer col of the row
        row_answer = row_dict[q_details[1]]
        # find additional answers that have the same q col values and put together the list
        all_answers = self.q_data.loc[
            (self.q_data[list(q_col_vals)] == pd.Series(q_col_vals)).all(axis=1),
            q_details[1],
        ].drop_duplicates()
        all_answers = all_answers.loc[lambda x: x != row_answer].to_list()
        all_answers.insert(0, row_answer)
        # create the question object
        return Question(
            q_text=q_text,
            answers=all_answers,
            a_col=q_details[1],
            allow_multiple_correct=allow_multiple_correct,
        )

    def gen_random_q(self, allow_multiple_correct: bool = False):
        """
        Generates a Question by picking a random unused row and random item from q_details.

        Args:
            allow_multiple_correct (bool, optional): Whether to display multiple correct answers. Defaults to False.

        Raises:
            ValueError: If all rows in q_data have been used already.

        Returns:
            Question: A Question object with attributes determined by the randomly chosen row and question details.
        """

        unused_rows = self.q_data[~self.q_data["row_used"]]

        if len(unused_rows.index) == 0:
            raise ValueError("Not enough unused data to generate question!")

        selected_row_id = unused_rows.sample(1).iloc[0].name

        selected_details = random.choice(self.q_details)

        q_to_return = self.gen_q_from_row(
            row_id=selected_row_id,
            q_details=selected_details,
            allow_multiple_correct=allow_multiple_correct,
        )

        self.mark_row_as_used(row_id=selected_row_id)

        return q_to_return

    def gen_alt_options(self, q_to_gen_for: Question, total_q_optns: int):
        """
        Generates alternative incorrect answers for a given question.

        Args:
            q_to_gen_for (Question): The question to generate alternative answers for.
            total_q_optns (int): The total number of options the question should have (including correct answers).

        Raises:
            ValueError: If more options are requested than can viably be generated by the function.

        Returns:
            list[str]: A list of the alternative answer options generated.
        """

        optns_needed = total_q_optns - len(q_to_gen_for.get_valid_answers())

        potential_alt_optns = self.q_data[q_to_gen_for.get_a_col()].drop_duplicates()

        potential_alt_optns = potential_alt_optns[
            ~potential_alt_optns.isin(q_to_gen_for.get_all_answers())
        ]

        if len(potential_alt_optns) < optns_needed:
            raise ValueError(
                f"{optns_needed} alternative options are needed, but only {len(potential_alt_optns)} are available."
            )

        alt_optns = potential_alt_optns.sample(optns_needed).to_list()

        return alt_optns

    def reset_used_rows(self):
        """Sets the row_used value for all rows in the q_data back to False."""
        self.q_data["row_used"] = False


class User:
    """Keeps track of a user's name, current lives and total score."""

    name: str
    lives: int
    score: int

    def __init__(self, name: str, lives: int = 3, score: int = 0):
        """
        Creates a new User.

        Args:
            name (str): The user's name.
            lives (int, optional): The number of lives the user should start with. Defaults to 3.
                Cannot be initialized as 0 or less.
            score (int, optional): The score the user should start with. Defaults to 0.
        """
        self.name = name
        if lives <= 0:
            raise ValueError("Lives cannot be initialized as 0 or less.")
        self.lives = lives
        self.score = score

    def get_name(self):
        """Returns the User's name."""
        return self.name

    def get_lives(self):
        """Returns the User's current number of lives."""
        return self.lives

    def get_score(self):
        """Returns the User's current score."""
        return self.score

    def add_score(self, to_add: int = 1):
        """Adds the given amount to the User's score. Adds 1 if no amount is given."""
        self.score += to_add

    def lose_lives(self, to_lose: int = 1):
        """
        Subtracts the given amount from the User's lives. Subtracts 1 if no amount is given.
        Sets lives to 0 if they would go below that.
        """
        if self.lives - to_lose < 0:
            self.lives = 0
        else:
            self.lives -= to_lose


class LeaderboardManager:
    """Manages the quiz's locally-stored leaderboard."""

    source_path: str
    board_size: int
    score_data: pd.DataFrame
    leader_chart: go.Figure

    def __init__(
        self,
        source_path: str = None,
        leaderboard_data: pd.DataFrame = None,
        score_col: str = "score",
        board_size: int = 5,
    ):
        """
        Creates a new LeaderboardManager.

        Args:
            source_path(str, optional): The filepath to a CSV source for the leaderboard. Defaults to None.
                Must be provided if leaderboard_data is None.
            leaderboard_data(pandas.DataFrame, optional): A DataFrame to use for the leaderboard data. Defaults to None.
                Must be provided if source_path is None.
            score_col (str, optional): The name of the column storing scores. Defaults to score.
            board_size (int, optional): The number of rows to include in the leaderboard. Defaults to 5.

        Raises:
            TypeError: If no leaderboard data is provided.
        """
        if leaderboard_data is not None:
            self.score_data = self.get_top_n(
                leaderboard_data, board_size, score_col=score_col
            )
        elif source_path is not None:
            self.source_path = source_path
            self.score_data = self.get_top_n(
                self.get_data_from_source(score_col=score_col),
                board_size,
                score_col=score_col,
            )
        else:
            raise TypeError(
                "No data source provided. Please provide either a DataFrame or a path to a CSV file."
            )
        self.board_size = board_size
        self.leader_chart = self.create_leader_chart()

    def get_score_data(self):
        """Returns the LeaderboardManager's score_data DataFrame."""
        return self.score_data

    def get_leader_chart(self):
        """Returns the LeaderboardManager's leader_chart Plotly figure."""
        return self.leader_chart

    def get_data_from_source(self, score_col: str = "score"):
        """
        Loads a DataFrame from the LeaderboardManager's source_path.
        Raises a TypeError if called while the object's source_path attribute is None.
        """
        if not self.source_path:
            raise TypeError(
                "Cannot retrieve data as this LeaderboardManager has no source_path."
            )
        return pd.read_csv(self.source_path)

    def get_top_n(
        self, data_to_filter: pd.DataFrame, n: int = 5, score_col: str = "score"
    ):
        "Returns the top n values in a given DataFrame, based off the given score_col."
        return data_to_filter.sort_values(
            by=score_col, ascending=False, ignore_index=True
        ).head(n)

    def create_leader_chart(
        self,
        user_col: str = "user",
        score_col: str = "score",
        bar_colour: str = "#006C7D",
    ):

        text_size = 18
        text_colour = "#000000"

        leaderboard_bar_chart = go.Bar(
            y=self.score_data.index,
            x=self.score_data[score_col],
            text=self.score_data[score_col],
            textposition="outside",
            marker={"color": bar_colour},
            orientation="h",
            hoverinfo="x+y",
            cliponaxis=False
        )

        leaderboard_chart_layout = go.Layout(
            font=dict(
                color=text_colour,
                size=text_size
            ),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            margin=dict(
                l=10,
                r=10,
                t=2,
                b=2,
                pad=2
            ),
            bargap=0.25,
            yaxis=dict(
                tickmode="array",
                tickvals=self.score_data.index,
                ticktext=self.score_data[user_col],
                autorange="reversed",
                tickfont = dict(
                    color=text_colour,
                    size=text_size
                ),
                automargin=True
            ),
            xaxis=dict(
                visible=False
            )
        )
        return go.Figure(leaderboard_bar_chart, layout=leaderboard_chart_layout)

    def save_row_to_source(self, row_to_add: pd.DataFrame):
        """Saves the given row DataFrame to the LeaderboardManager's source."""
        if self.source_path is None:
            raise TypeError(
                "Cannot save data as this LeaderboardManager has no source_path."
            )
        row_to_add.to_csv(self.source_path, mode="a", index=False, header=False)

    def save_result_and_update(
        self, user_to_add: User, user_col: str = "user", score_col: str = "score"
    ):
        """Updates leaderboards with the given User's results and saves them to the file if applicable."""

        new_result_row = pd.DataFrame(
            {user_col: [user_to_add.get_name()], score_col: [user_to_add.get_score()]}
        )

        if self.source_path is not None:
            self.save_row_to_source(new_result_row)

        # replace the score at the bottom of the leaderboard with the user's name and score
        self.score_data = self.score_data.iloc[:-1]
        self.score_data = pd.concat([self.score_data, new_result_row])
        self.score_data = self.score_data.sort_values(
            by=score_col, ascending=False, ignore_index=True
        )
        self.leader_chart = self.create_leader_chart()


class StringInputChecker:
    """Can run various checks on string inputs."""

    max_len: int
    format_regex: str

    def __init__(self, max_len: int, format_regex: str):
        """
        Creates a new StringInputChecker.

        Args:
            max_len(int): The maximum length allowed for the input.
            format_regex(str): A regular expression to check the string's format against.
        """
        self.max_len = max_len
        self.format_regex = format_regex

    def presence_check(self, input_to_check: str):
        """Performs a presence check against the given input."""
        if input_to_check is None:
            return False
        else:
            return bool(input_to_check.strip())

    def length_check(self, input_to_check: str):
        """Checks the length of the given input against the StringInputChecker's max_len attribute."""
        return len(input_to_check) <= self.max_len

    def format_check(self, input_to_check: str):
        """Checks the format of the given input against the StringInputChecker's format_regex."""
        return bool(re.fullmatch(self.format_regex, input_to_check))
