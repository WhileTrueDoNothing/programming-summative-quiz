"""Tools for creating questions and quizzes."""

from random import shuffle              # for shuffling multiple choice options
from random import randint              # for selecting random items from a list
from string import ascii_lowercase      # for generating the index for multiple choice options
import pandas as pd                     # for importing and managing question data
import numpy as np                      # for condensing filter conditions
import string                           # for handling custom question strings


class Question:
    """A question that can be answered by a free text input."""

    question: str
    answers: list[str]

    def __init__(self, question, answers):
        """
        Create a new Question.

        Args:
            question (str): The text for the question to be asked.
            answers (list[str]): The correct answer(s) for the question.
        """
        self.question = question
        self.answers = answers

    def ask(self):
        """
        Asks the user the question. Returns 1 if the user inputs the correct answer, or 0 otherwise.
        """

        print(self.question)
        user_answer = input("Your answer: ")

        if user_answer.lower() in [answer.lower() for answer in self.answers]:
            print("Correct!")
            return 1
        else:
            print("Incorrect! The answer was {}".format(self.answers[0]))
            return 0


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
        shuffle(all_options)

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
        score += (questions[i].ask() * score_per_question)

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
        selected_q = q_details[randint(0, len(q_details) - 1)]


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
                options_to_add = q_df[~q_df["row_used"] & ~q_df[a_col].isin(q_answers) & ~q_df[a_col].isin(q_incorrect)].sample(options_needed)
                options_to_add.drop_duplicates(subset=a_col)

                q_incorrect.extend(options_to_add[a_col].to_list())

                # flag rows as used
                q_df.loc[q_df.index.isin(options_to_add), "row_used"] = True

                options_needed = multi_choice_options - len(q_answers) - len(q_incorrect)

            # save details as MultiChoiceQuestion object
            q_list.append(MultiChoiceQuestion(q_text, q_answers, q_incorrect))

        else:
            # save details as Question object
            q_list.append(Question(q_text, q_answers))

    print("Ready!")
    return q_list
