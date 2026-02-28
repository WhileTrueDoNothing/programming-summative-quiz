"""Tools for creating questions and quizzes."""

import random # for picking random items from lists
from string import (
    ascii_lowercase,
)  # for generating the index for multiple choice options
import pandas as pd  # for importing and managing question data
import numpy as np  # for condensing filter conditions
import string  # for handling custom question strings


class Question:
    """A question that can be answered by a free text input."""

    q_text: str
    answers: list[str]
    a_col: str
    allow_multiple_correct: bool

    def __init__(self, q_text: str, answers: list[str], a_col: str, allow_multiple_correct: bool = False):
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
        """Checks a given input against a list of the Question's answer(s). Returns True if the input is present, False otherwise."""
        valid_answers = self.get_valid_answers()

        if a_to_check.lower() in [answer.lower() for answer in valid_answers]:
            return True
        else:
            return False


class QuestionGenerator:
    """A class that stores and generates questions from a Pandas DataFrame."""

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
            q_details (tuple[tuple[str,str]]): Question details. The first item in a pair should be a formattable string for the question text, with column names in {} where their value should be. Second value is the name of the column to get the answer from.
            q_data (pandas.DataFrame, optional*): A DataFrame to generate questions from. Must be supplied if q_data_source_path is None. Defaults to None.
            q_data_source_path (str, optional*): The path to a CSV file to generate question data from. Must be supplied if q_data is None. Defaults to None.
        """

        self.q_details = q_details

        if q_data is not None:
            self.q_data = q_data
        elif q_data_source_path is not None:
            self.q_data = pd.read_csv(q_data_source_path, index_col=None)
        else:
            raise TypeError(
                "No question data was provided. Please provide either a DataFrame or a filepath to a CSV file."
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
        colname_list =  [
        span[1]
        for span in string.Formatter().parse(text)
        if span[1] is not None
        ]
        return list(set(colname_list))

    def mark_row_as_used(self, row_id: int):
        """Sets the value of row_used for a given row_id to True."""
        self.q_data.loc[row_id, "row_used"] = True

    def gen_q_from_row(self, row_id: int, q_details: tuple[str,str], allow_multiple_correct: bool = False):
        """
        Generates a Question from the specified row and details.

        Args:
            row_id (int): The index of the row to create a question from.
            q_details (tuple[str,str]): The question text and answer column to be used for the question.
            allow_multiple_correct (bool, optional): Whether to display multiple correct answers. Defaults to False.

        Returns:
            Question: A Question object with the q_text, answers, a_col and allow_multiple_correct attributes determined by the inputs provided.
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
        all_answers = self.q_data.loc[(self.q_data[list(q_col_vals)] == pd.Series(q_col_vals)).all(axis=1), q_details[1]].drop_duplicates()
        all_answers = all_answers.loc[lambda x : x != row_answer].to_list()
        all_answers.insert(0,row_answer)
        # create the question object
        return Question(q_text=q_text, answers=all_answers, a_col=q_details[1], allow_multiple_correct=allow_multiple_correct)
    
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

        q_to_return = self.gen_q_from_row(row_id=selected_row_id, q_details=selected_details, allow_multiple_correct=allow_multiple_correct)

        self.mark_row_as_used(row_id = selected_row_id)

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

        potential_alt_optns = potential_alt_optns[~potential_alt_optns.isin(q_to_gen_for.get_all_answers())]

        if len(potential_alt_optns) < optns_needed:
            raise ValueError(f"{optns_needed} alternative options are needed, but only {len(potential_alt_optns)} are available.")
        
        alt_optns = potential_alt_optns.sample(optns_needed).to_list()

        return alt_optns

    def reset_used_rows(self):
        """Sets the row_used value for all rows in the q_data back to False."""
        self.q_data["row_used"] = False

class User():
    pass

class LeaderboardManager():
    pass

class MultiChoiceQuestion(Question):
    """A multiple choice question. Supports up to 26 options."""

    wrong_answers: list[str]

    def __init__(self, question, answers, wrong_answers):
        """
        Create a new MultiChoiceQuestion.

        Args:
            question (str): The text for the question to be asked.
            answers (list[str]): The correct answer(s) for the question.
            wrong_answers (list[str]): Other options for the question.

        Raises:
            ValueError: If the combined length of correct and incorrect answer lists is higher than 26.
        """

        if len(answers) + len(wrong_answers) > 26:
            raise ValueError(
                "Combined length of correct and incorrect answer lists must be 26 or less. Total options received: {total}".format(
                    total=len(answers) + len(wrong_answers)
                )
            )
        self.wrong_answers = wrong_answers
        super().__init__(question, answers)

    def ask(self):
        """
        Asks the user the question, loops until an option is selected. Returns 1 if the user inputs the correct answer, or 0 otherwise.
        """

        all_options = self.answers + self.wrong_answers
        random.shuffle(all_options)

        option_list = {}

        for letter, option in zip(list(ascii_lowercase), all_options):
            option_list[letter] = option

        full_question_text = (
            self.question
            + "\n"
            + "\n".join(
                "{index}) {option}".format(index=key, option=value)
                for key, value in option_list.items()
            )
        )

        print(full_question_text)

        valid_input = False

        while not valid_input:
            user_answer = input("Your answer: ")

            if user_answer.lower() in option_list.keys():
                valid_input = True
                if option_list[user_answer.lower()] in self.answers:
                    print("Correct!")
                    return 1
                else:
                    print("Incorrect! The answer was {}".format(self.answers[0]))
                    return 0
            elif user_answer.lower() in [
                option.lower() for option in option_list.values()
            ]:
                valid_input = True
                if user_answer.lower() in [answer.lower() for answer in self.answers]:
                    print("Correct!")
                    return 1
                else:
                    print("Incorrect! The answer was {}".format(self.answers[0]))
                    return 0
            else:
                print("Please enter one of the options!")

        # The function should exit during the while loop, this is here in case it does not
        print("How is this method still running?")
        return 0


def run_quiz(
    questions: list[Question],
    score_per_question: int = 1,
    question_separator: str = "-----------",
    first_question_num: int = 1,
):
    """
    Runs a quiz.

    Args:
        questions (list[Question]): The list of questions to ask.
        score_per_question (int, optional): The score for a correct answer. Defaults to 1.
        question_separator (str, optional): A string to separate questions in the terminal. Defaults to -----------.
        first_question_num (int, optional): The number of the first question in the quiz. Defaults to 1.

    Returns:
        int: The total score for the quiz.

    Raises:
        ValueError: If the questions argument is an empty list.
    """

    if len(questions) == 0:
        raise ValueError("No questions provided for the quiz!")

    score = 0

    for i in range(0, len(questions)):
        print(question_separator)
        print("Question {q_num}".format(q_num=i + first_question_num))
        print(question_separator)
        score += questions[i].ask() * score_per_question

    print(question_separator)
    print("Your score: {total}".format(total=score))
    print(question_separator)
    return score


def extract_placeholders(string_to_extract: str):
    """Extracts the {placeholder} names from a string and returns them as a list."""

    return [
        span[1]
        for span in string.Formatter().parse(string_to_extract)
        if span[1] is not None
    ]


def gen_questions_csv(
    source_path: str,
    q_details: list[tuple[str, str]],
    multi_choice: bool = True,
    num_questions: int = 10,
    multi_choice_options: int = 4,
):
    """
    Loads a provided CSV file into a dataframe and uses it to generate questions for the quiz.

    Args:
        source_path (str): The name/path of the file to load question data from.
        q_details (list[tuple[str,str]]): The first item in a pair should be a formattable string for the question text, with column names in {} where their value should be. Second value is the name of the column to get the answer from.
        multi_choice (bool, optional): Generates multiple choice questions if True, free text ones if False. Default is True.
        num_questions (int, optional): The number of questions to generate. Default is 10.
        multi_choice_options (int, optional): The number of options to generate for a multiple choice question. Default is 4.

    Returns:
        list[Question]: A list of Question objects that can be used for a quiz.

    Raises:
        ValueError: If more questions than can be provided by the data are requested, or if the function runs out of unused rows of data while generating questions.
        KeyError: If a column name provided in q_details can't be found in the dataframe.
    """

    print("Generating questions...")

    q_df = pd.read_csv(source_path)

    # make sure there aren't more questions than rows in the dataframe
    # or more options needed for multiple choice questions than rows in the data
    if (num_questions > len(q_df.index)) or (
        multi_choice and num_questions * multi_choice_options > len(q_df.index)
    ):
        raise ValueError("Too many questions requested for the size of data provided!")

    # get columns needed for question and answer
    cols_to_use = set()

    for q, a in q_details:
        cols_to_use.update(extract_placeholders(q))
        cols_to_use.add(a)

    # select only needed columns from dataframe
    # throw an error if a provided column name doesn't exist in the data
    try:
        q_df = q_df[list(cols_to_use)]
    except KeyError as e:
        raise KeyError("An error occurred: {}".format(e))

    # add "used" flag column to dataframe
    q_df = q_df.assign(row_used=False)

    q_list = []

    # for each question
    for i in range(0, num_questions):
        # pick random question type from the question details list
        selected_q = q_details[random.randint(0, len(q_details) - 1)]

        # get the column(s) used for the question
        q_cols = extract_placeholders(selected_q[0])
        a_col = selected_q[1]

        unused_rows = q_df[~q_df["row_used"]]

        if len(unused_rows.index) == 0:
            raise ValueError("Not enough unused data to generate question!")

        # pick random row from data, pack question column values into a dictionary
        q_text_dict = unused_rows.sample()[q_cols].to_dict("records")[0]

        # generate text for the question
        q_text = selected_q[0].format(**q_text_dict)

        # create conditions to filter for answers
        conditions = []
        for col, val in q_text_dict.items():
            conditions.append(q_df[col] == val)

        conds_reduced = np.logical_and.reduce(conditions)

        # get answer values from answer column, filtering by selected question column values
        q_answers = q_df.loc[conds_reduced, a_col].drop_duplicates().to_list()

        # flag rows as used
        q_df.loc[conds_reduced, "row_used"] = True

        if multi_choice:
            options_needed = multi_choice_options - len(q_answers)
            q_incorrect = []

            while options_needed > 0:
                if len(q_df[~q_df["row_used"]].index) < options_needed:
                    raise ValueError("Not enough unused data to generate question!")

                # get random incorrect options
                options_to_add = q_df[
                    ~q_df["row_used"]
                    & ~q_df[a_col].isin(q_answers)
                    & ~q_df[a_col].isin(q_incorrect)
                ].sample(options_needed)
                options_to_add.drop_duplicates(subset=a_col)

                q_incorrect.extend(options_to_add[a_col].to_list())

                # flag rows as used
                q_df.loc[q_df.index.isin(options_to_add), "row_used"] = True

                options_needed = (
                    multi_choice_options - len(q_answers) - len(q_incorrect)
                )

            # save details as MultiChoiceQuestion object
            q_list.append(MultiChoiceQuestion(q_text, q_answers, q_incorrect))

        else:
            # save details as Question object
            q_list.append(Question(q_text, q_answers))

    print("Ready!")
    return q_list
