# Postcode Area Quiz
# Introduction
This app is a quiz for improving knowledge on UK postcode areas by asking randomly generated questions until you run out of lives. The first questions ask you to pick from only 4 random options, but as you score more points you'll be asked to pick from a complete list of options and eventually type answers yourself with no hints provided!

## Setup instructions
The app currently can only run locally, so you'll have to install and run it yourself.
### 1. Clone the repository
Using your terminal/command line, navigate to the folder you want to save the repository to and use:
```
git clone https://github.com/WhileTrueDoNothing/programming-summative-quiz
```
### 2. Install dependencies
```
pip install -r requirements.txt
```
### 3. Run the project
Navigate to the app's folder and run it with:
```
streamlit run main.py
```
It takes a few seconds to start, but it'll then open in a tab in your browser.
# Design
## Requirements
### Must
The application must:
- Generate questions randomly from the postcode data.
- Save and store user scores so they can be accessed later.
- Validate user name inputs to ensure they don't contain numbers or symbols.
- Either end the quiz or reset the data if all question data has been used.
### Should
The application should:
- Display the leaderboard as a graph.
- Contain a widget explaining how to play the game.
- Use a contrasting colour palette tested with a colour blindness simulator.
- Ensure that questions don't accidentally provide a correct answer as an incorrect option. (for example, if both SW and EC were labelled London, if SW was the intended answer then EC should either not be a selectable option or accepted as correct.)
### Could
The application could:
- Become more difficult once the user scores enough points by offering a selection menu of all options instead of just 4.
- Become even more difficult for high scoring users by switching to just a free text input.
### Won't
(This version of) the application won't:
- Utilize postcode district data for questions. That dataset is too large and complex to be worth implementing at this stage.
- Differentiate between users with the same score by other metrics. Choosing and implementing an alternative metric takes time, and I have higher priority tasks.
- Score users based on the time they take to answer (to deter them from googling it). The time it could take to implement the system and find ideal time limits outweighs the value it could bring.

## Initial plans
Before creating the prototype, I drew some initial plans for the interface in my notebook.
<img width="691" height="922" alt="Initial drawings of the quiz interface." src="https://github.com/user-attachments/assets/43e58ede-6182-4e5b-a3f7-75f73b92cef7" />


## Prototype
I used figma to create a prototype of the user's journey through the quiz. It demonstrates viewing instructions on how to play, entering a user's name, answering a question and the quiz leaderboard updating with their final score. It can be accessed [here](https://www.figma.com/design/uioibs1bjv756tDAnCv9xo/postcode_quiz_ui_prototype?node-id=0-1&t=zjcT6pKWqf88Nzvt-1).
<img width="1186" height="1077" alt="The Figma UI prototype for the quiz, showing the flow between different screens." src="https://github.com/user-attachments/assets/6b433fee-1b68-4114-8511-8fa7dbb06c68" />

I chose teal, orange, black and white as the main interface colours as they're of contrasting hues and follow my company's design brand guidelines. I used [a palette checker](https://palettechecker.com/) to ensure they'd still contrast if a user was colourblind.
<img width="902" height="461" alt="A colour blindness simulation, showing the colour contrast for 3 common types of colour blindness." src="https://github.com/user-attachments/assets/5efce0bd-65af-471f-add7-6aaa5d0cb2b1" />

### Libraries used

|Component|Library|
|---------|---------|
|GUI|Streamlit, CSS|
|Data visualisation|Plotly Graph Objects|
|Data management|Pandas|

I chose streamlit for the interface as I'm familiar with the library, and with external data integration I could easily deploy the app to their Community Cloud. Plotly visualisations are highly customizeable and interactive. I chose plotly graph objects over plotly express to allow more fine-tuning of my chart. Pandas is a powerful tool for handling datasets. Its CSV functions make reading and writing to files incredibly simple.

### Classes
I haven't included the full details of classes I didn't make.

<img width="1071" height="774" alt="summative_quiz_class_diagram" src="https://github.com/user-attachments/assets/6128ffb9-ae76-4eaf-876f-8310418798bb" />


# Development
To start with, I had the code from [the command line version of the quiz](https://github.com/WhileTrueDoNothing/programming-formative-quiz). This contained classes for questions, along with functions for generating questions from a given CSV file and running a quiz. However, many of these functions needed breaking down into smaller ones.

## quiz_utils module
I began development with the quiz_utils module, as a lot of the code could be reconstructed from the quiz's command line version. I first constructed a basic class diagram to plan my classes and their functions, with plans to amend it during development, should I need to.

<img width="796" height="518" alt="A draw.io diagram with details on the User, LeaderboardManager, Question and QuestionGenerator classes." src="https://github.com/user-attachments/assets/910f75be-7cdb-4e17-8a35-fda432d2c097" />

### Question

```python
class Question(builtins.object)
     |  Question(q_text: str, answers: list[str], a_col: str, allow_multiple_correct: bool = False)
     |  
     |  A question that can be answered by a free text input.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, q_text: str, answers: list[str], a_col: str, allow_multiple_correct: bool = False)
     |      Create a new Question.
     |      
     |      Args:
     |          q_text (str): The text for the question to be asked.
     |          answers (list[str]): The correct answer(s) for the question.
     |          a_col (str): The column in the data the answer is from (for generating options to select from).
     |          allow_multiple_correct (bool, optional): Whether to display multiple correct answers.
     |  
     |  check_answer(self, a_to_check: str)
     |      Checks a given input against a list of the Question's answer(s).
     |      Returns True if the input is present, False otherwise.
     |  
     |  get_a_col(self)
     |      Returns the name of the column the Question's answers are from.
     |  
     |  get_all_answers(self)
     |      Returns the list of all the Question's answers, no matter the value of allow_multiple_correct.
     |  
     |  get_q_text(self)
     |      Returns the question's text.
     |  
     |  get_valid_answers(self)
     |      Returns the full list of answers if allow_multiple_correct is true, returns only the first otherwise.
```

I developed Question first. Classes like QuestionGenerator relied on it's existence, and the specifics of many other app elements depended on the way I decided to implement it. Alongside the question's text and correct answers, I decided to store the name of the column used for the answer. This allows the QuestionGenerator to generate incorrect multiple choice answers without needing to store them in the class itself. It also allowed me to easily retrieve the column to use as options for selectbox type questions.

I added allow_multiple_correct slightly later, upon realising the QuestionGenerator needed to know all potential answers to the given question, even if only one were to be displayed. If a single value was stored, other correct values could be selected as "incorrect" options. With allow_multiple_correct set to False, the Question will store all potential answers to avoid this, while only outputting the first answer if a single one is needed.

```python
def get_valid_answers(self):
        """Returns the full list of answers if allow_multiple_correct is true, returns only the first otherwise."""
        if self.allow_multiple_correct:
            return self.answers
        else:
            return self.answers[:1]
```

### QuestionGenerator

```python
class QuestionGenerator(builtins.object)
     |  QuestionGenerator(q_details: tuple[tuple[str, str]], q_data: pandas.core.frame.DataFrame = None, q_data_source_path: str = None)
     |  
     |  Manages a pandas DataFrame and uses it to generate Question objects.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, q_details: tuple[tuple[str, str]], q_data: pandas.core.frame.DataFrame = None, q_data_source_path: str = None)
     |      Creates a new QuestionGenerator.
     |      
     |      Args:
     |          q_details (tuple[tuple[str,str]]): Question details. The first item in the tuple should be a formattable
     |              string for the question text, with column names in {} where their value should be. Second value is
     |              the name of the column to get the answer from.
     |          q_data (pandas.DataFrame, optional*): A DataFrame to generate questions from. Defaults to None.
     |              Must be provided if q_data_source_path is None.
     |          q_data_source_path (str, optional*): The path to a CSV file containing question data. Defaults to None.
     |              Must be provided if q_data is None.
     |      
     |      Raises:
     |          TypeError: If no question data is provided.
     |  
     |  gen_alt_options(self, q_to_gen_for: quiz_utils.Question, total_q_optns: int)
     |      Generates alternative incorrect answers for a given question.
     |      
     |      Args:
     |          q_to_gen_for (Question): The question to generate alternative answers for.
     |          total_q_optns (int): The total number of options the question should have (including correct answers).
     |      
     |      Raises:
     |          ValueError: If more options are requested than can viably be generated by the function.
     |      
     |      Returns:
     |          list[str]: A list of the alternative answer options generated.
     |  
     |  gen_q_from_row(self, row_id: int, q_details: tuple[str, str], allow_multiple_correct: bool = False)
     |      Generates a Question from the specified row and details.
     |      
     |      Args:
     |          row_id (int): The index of the row to create a question from.
     |          q_details (tuple[str,str]): The question text and answer column to be used for the question.
     |          allow_multiple_correct (bool, optional): Whether to display multiple correct answers. Defaults to False.
     |      
     |      Returns:
     |          Question: A Question object with the q_text, answers, a_col and allow_multiple_correct attributes
     |          determined by the inputs provided.
     |  
     |  gen_random_q(self, allow_multiple_correct: bool = False)
     |      Generates a Question by picking a random unused row and random item from q_details.
     |      
     |      Args:
     |          allow_multiple_correct (bool, optional): Whether to display multiple correct answers. Defaults to False.
     |      
     |      Raises:
     |          ValueError: If all rows in q_data have been used already.
     |      
     |      Returns:
     |          Question: A Question object with attributes determined by the randomly chosen row and question details.
     |  
     |  get_colnames_from_text(self, text: str)
     |      Extracts column names from {curly brackets} in a string and returns them as a list.
     |  
     |  get_q_data(self)
     |      Returns the QuestionGenerator's q_data DataFrame.
     |  
     |  get_q_details(self)
     |      Returns the QuestionGenerator's q_details tuple tuple.
     |  
     |  mark_row_as_used(self, row_id: int)
     |      Sets the value of row_used for a given row_id to True.
     |  
     |  reset_used_rows(self)
     |      Sets the row_used value for all rows in the q_data back to False.
```

This is the most complicated class, requiring many methods to manage its DataFrame and generate Questions. While I had planned to only initialize DataFrames from CSV files, I realised that allowing a DataFrame to be input directly would make testing easier. Breaking down the question generation functions into smaller, more specific methods also helped with this. The command line quiz generated all its questions in a single, overly-complicated function. QuestionGenerator instead contains a method to generate a Question from a specific row and a method to mark a specific row as used, which can both be easily tested. They can then both be called by another method that selects the random row and details they are to use.

```python
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
```

The gen_alt_options method relies on the Question's allow_multiple_correct attribute to handle duplicates in the question or answer columns. When calculating the number of options it needs to generate, it'll only count the Question's "valid" answer(s). However, when selecting potential alternative options, it ignores *all* potential correct answers, regardless of allow_multiple_correct's value. This prevents it from selecting an "incorrect" option that's actually correct.

```python
optns_needed = total_q_optns - len(q_to_gen_for.get_valid_answers())

        potential_alt_optns = self.q_data[q_to_gen_for.get_a_col()].drop_duplicates()

        potential_alt_optns = potential_alt_optns[
            ~potential_alt_optns.isin(q_to_gen_for.get_all_answers())
        ]
```

### User
```python
class User(builtins.object)
     |  User(name: str, lives: int = 3, score: int = 0)
     |  
     |  Keeps track of a user's name, current lives and total score.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, name: str, lives: int = 3, score: int = 0)
     |      Creates a new User.
     |      
     |      Args:
     |          name (str): The user's name.
     |          lives (int, optional): The number of lives the user should start with. Defaults to 3.
     |              Cannot be initialized as 0 or less.
     |          score (int, optional): The score the user should start with. Defaults to 0.
     |  
     |  add_score(self, to_add: int = 1)
     |      Adds the given amount to the User's score. Adds 1 if no amount is given.
     |  
     |  get_lives(self)
     |      Returns the User's current number of lives.
     |  
     |  get_name(self)
     |      Returns the User's name.
     |  
     |  get_score(self)
     |      Returns the User's current score.
     |  
     |  lose_lives(self, to_lose: int = 1)
     |      Subtracts the given amount from the User's lives. Subtracts 1 if no amount is given.
     |      Sets lives to 0 if they would go below that.
```
This class stores and manages details on the current user playing the quiz. My main concern when creating this class was preventing the user's lives from being set to less than zero, to avoid issues displaying lives in the interface. The constructor method throws a ValueError if the initial lives value is 0 or less, to avoid ending the quiz immediately. The User's lives can be set to 0 by the lose_lives method, and will be set to 0 if the subtracted value would be less than that.

### LeaderboardManager
```python
class LeaderboardManager(builtins.object)
     |  LeaderboardManager(source_path: str = None, leaderboard_data: pandas.core.frame.DataFrame = None, score_col: str = 'score', board_size: int = 5)
     |  
     |  Manages the quiz's locally-stored leaderboard.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, source_path: str = None, leaderboard_data: pandas.core.frame.DataFrame = None, score_col: str = 'score', board_size: int = 5)
     |      Creates a new LeaderboardManager.
     |      
     |      Args:
     |          source_path(str, optional): The filepath to a CSV source for the leaderboard. Defaults to None.
     |              Must be provided if leaderboard_data is None.
     |          leaderboard_data(pandas.DataFrame, optional): A DataFrame to use for the leaderboard data. Defaults to None.
     |              Must be provided if source_path is None.
     |          score_col (str, optional): The name of the column storing scores. Defaults to score.
     |          board_size (int, optional): The number of rows to include in the leaderboard. Defaults to 5.
     |      
     |      Raises:
     |          TypeError: If no leaderboard data is provided.
     |  
     |  create_leader_chart(self, user_col: str = 'user', score_col: str = 'score', bar_colour: str = '#006C7D')
     |  
     |  get_data_from_source(self, score_col: str = 'score')
     |      Loads a DataFrame from the LeaderboardManager's source_path.
     |      Raises a TypeError if called while the object's source_path attribute is None.
     |  
     |  get_leader_chart(self)
     |      Returns the LeaderboardManager's leader_chart Plotly figure.
     |  
     |  get_score_data(self)
     |      Returns the LeaderboardManager's score_data DataFrame.
     |  
     |  get_top_n(self, data_to_filter: pandas.core.frame.DataFrame, n: int = 5, score_col: str = 'score')
     |      Returns the top n values in a given DataFrame, based off the given score_col.
     |  
     |  save_result_and_update(self, user_to_add: quiz_utils.User, user_col: str = 'user', score_col: str = 'score')
     |      Updates leaderboards with the given User's results and saves them to the file if applicable.
     |  
     |  save_row_to_source(self, row_to_add: pandas.core.frame.DataFrame)
     |      Saves the given row DataFrame to the LeaderboardManager's source.
```

This class loads and manages the leaderboard data, currently stored locally in a CSV file. I decided to limit the number of rows in the DataFrame to keep it to a reasonable size. I chose to make the leaderboard chart a Plotly figure for its interactivity and customizeability. I added an option for direct DataFrame input to the class alongside the CSV file, to make it easier to input data from external sources in the future.

When saving a new user's results, I've decided to always include them in the DataFrame so they can see themselves on the leaderboard at the end. I achieve this by removing the bottom row from the score data before adding the new row and sorting the DataFrame.

```python
# replace the score at the bottom of the leaderboard with the user's name and score
        self.score_data = self.score_data.iloc[:-1]
        self.score_data = pd.concat([self.score_data, new_result_row])
        self.score_data = self.score_data.sort_values(
            by=score_col, ascending=False, ignore_index=True
        )
        self.leader_chart = self.create_leader_chart()
```

### StringInputChecker
```python
class StringInputChecker(builtins.object)
     |  StringInputChecker(max_len: int, format_regex: str)
     |  
     |  Can run various checks on string inputs.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, max_len: int, format_regex: str)
     |      Creates a new StringInputChecker.
     |      
     |      Args:
     |          max_len(int): The maximum length allowed for the input.
     |          format_regex(str): A regular expression to check the string's format against.
     |  
     |  format_check(self, input_to_check: str)
     |      Checks the format of the given input against the StringInputChecker's format_regex.
     |  
     |  length_check(self, input_to_check: str)
     |      Checks the length of the given input against the StringInputChecker's max_len attribute.
     |  
     |  presence_check(self, input_to_check: str)
     |      Performs a presence check against the given input.
```

This class validates text inputs with its methods. It'll allow me to keep input requirements consistent by only needing to declare them once per object.

## streamlit frontend
### session states and dynamic widgets
Streamlit reruns all code any time a change is made. To prevent repeated loading, I stored the classes I'd created in the session state. I also used session states to control what the app loaded on a given run, as shown in the page's middle column:

```python```
with col2:
    st.title("UK Postcode Quiz", text_alignment="center")
    if st.session_state.app_state in ["start_pg", "end_pg"]:
        if st.session_state.app_state == "end_pg":
            st.subheader("Your final score: {}".format(st.session_state.prev_usr_score))
        st.header("Leaderboard", text_alignment="center")
        st.plotly_chart(st.session_state.leaderboard_mgr.get_leader_chart())
        render_name_form()
    if st.session_state.app_state in ["q_ask", "q_correct", "q_incorrect"]:
        st.header("Question {}".format(st.session_state.q_num))
        st.subheader(st.session_state.current_q.get_q_text())
        render_a_input()
        if st.session_state.app_state in ["q_correct", "q_incorrect"]:
            render_result_msg()
            render_next_btn()
```

I rendered certain widgets dynamically using functions. For example, the type of widget used to answer questions is determnined by a session state.

```python
def render_a_input():
    """Renders the answer input for the quiz, depending on the session state."""
    if st.session_state.current_q_type == "text":
        st.text_input(
            label="Enter your answer:",
            label_visibility="collapsed",
            disabled=(st.session_state.app_state in ["q_correct", "q_incorrect"]),
            placeholder="Enter your answer...",
            on_change=check_answer_and_update,
            key="selected_a",
        )
    elif st.session_state.current_q_type == "selectbox":
        st.selectbox(
            label="Select an option:",
            options=st.session_state.current_q_opts,
            accept_new_options=False,
            disabled=(st.session_state.app_state in ["q_correct", "q_incorrect"]),
            on_change=check_answer_and_update,
            key="selected_a",
        )
    else:
        st.radio(
            label="Select an option:",
            options=st.session_state.current_q_opts,
            disabled=(st.session_state.app_state in ["q_correct", "q_incorrect"]),
            on_change=check_answer_and_update,
            key="selected_a",
        )
```

The current_q_type session state is determined in the starT_new_q function, which generates different question types depending on the user's score. It will also reset used rows in the question generator's data if they run out (thus throwing a TypeError).

```python
def start_new_q():
    """
    Generates a new question and resets the data if all rows have been used.
    Generates different types of question depending on the score:
        - Generates for a free-text input for scores higher than 20.
        - Generates for a select box for scores higher than 10.
        - Generates for 4-item radio buttons for lower scores.
    """
    st.session_state.q_num += 1
    if st.session_state.current_usr.get_score() > 20:
        st.session_state["current_q_type"] = "text"
        try:
            st.session_state.current_q = st.session_state.q_gen.gen_random_q(
                allow_multiple_correct=True
            )
        except TypeError:
            st.session_state.q_gen.reset_used_rows()
            st.session_state.current_q = st.session_state.q_gen.gen_random_q(
                allow_multiple_correct=True
            )
        st.session_state.current_q_opts = None
    elif st.session_state.current_usr.get_score() > 10:
        st.session_state["current_q_type"] = "selectbox"
        try:
            st.session_state.current_q = st.session_state.q_gen.gen_random_q(
                allow_multiple_correct=True
            )
        except TypeError:
            st.session_state.q_gen.reset_used_rows()
            st.session_state.current_q = st.session_state.q_gen.gen_random_q(
                allow_multiple_correct=True
            )
        st.session_state.current_q_opts = st.session_state.q_gen.get_q_data()[
            st.session_state.current_q.get_a_col()
        ].drop_duplicates()
    else:
        st.session_state["current_q_type"] = "radio"
        try:
            st.session_state.current_q = st.session_state.q_gen.gen_random_q(
                allow_multiple_correct=False
            )
        except TypeError:
            st.session_state.q_gen.reset_used_rows()
            st.session_state.current_q = st.session_state.q_gen.gen_random_q(
                allow_multiple_correct=False
            )
        alt_q_opts = st.session_state.q_gen.gen_alt_options(
            st.session_state.current_q, total_q_optns=4
        )
        st.session_state.current_q_opts = (
            alt_q_opts + st.session_state.current_q.get_valid_answers()
        )
        shuffle(st.session_state.current_q_opts)

    st.session_state.app_state = "q_ask"
```
### Custom themeing
A notable issue with Streamlit is how difficult it is to customize the styles of pages. Theme colours can be declared in the `.streamlit/config.toml` file [as described in their documentation.](https://docs.streamlit.io/develop/api-reference/configuration/config.toml#theme)

```
[theme]
backgroundColor = "#57C5C6"
secondaryBackgroundColor = "#ffffff"
primaryColor = "#e9A200"
textColor = "#000000"
```

For finer control of colours, you must use CSS inside HTML style tags inside a HTML-enabled streamlit markdown container. This is complicated and may break in future updates, but it's currently the only way to do it.

```python
st.markdown(
    """
    <style>
    div[data-testid="stExpander"]{
        background-color: #e9A200;
        color: #000000;
        border: 1px solid #000000;
        border-radius: 0.5rem;
    }
    div[data-testid="stExpander"] > details {
        border-style: none;
    }
    div[data-testid="stExpander"] > details > summary {
        background-color: #e9A200;
        color: #000000;
    }
    div[data-testid="stExpanderDetails"] {
        background-color: #ffffff;
        color: #000000;
        border-radius: 0px 0px 0.5rem 0.5rem;
    }
    div[data-testid="stAlertContentError"]{
        color: #000000;
    }
    button[kind="secondaryFormSubmit"]{
        background-color: #e9A200;
        color: #000000;
        border: 1px solid #000000;
        border-radius: 0.5rem;
    }
    button[kind="secondary"]{
        background-color: #e9A200;
        color: #000000;
        border: 1px solid #000000;
        border-radius: 0.5rem;
    }
    li[role="option"]{
        background-color: #ffffff;
    }
    div[data-testid="stMarkdownContainer"] {
        font-size: 20px
    }
    </style>
    """,
    unsafe_allow_html=True,
)
```

To work out which elements to style, I used inspect element while running the app to browse its HTML. I tried setting styles for a particular element, then reran the code again to see if it worked.

# Testing
## Unit Tests
I used pytest to ensure my classes and functions worked as expected. I chose pytest over unittest due to it's easy Github integration and the lack of boilerplate code required when creating tests. I used a separate file for each class to keep my tests organized.

### Question
Question was a fairly simple class to test. I started with a smoke test to ensure things were working properly, then used two almost-identical fixtures to ensure the allow_multiple_correct attribute properly affected the answer checking.

```python
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
```

### QuestionGenerator
Adding a direct DataFrame parameter for initializing QuestionGenerators let me run tests with a specially designed DataFrame fixture. By having duplicate values in both columns of ez_maths_df, I could ensure the QuestionGenerator could properly handle questions with multiple correct answers and vice versa. It also meant that gen_alt_options would always output the same "random" sample (as only 2 options were valid to select), letting me test against that.

```python
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
```

### User
The tests for this class ensured its attributes were properly initialized and managed by its methods, whether values were provided or defaults were used.

```python
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
```

### LeaderboardManager
For these tests, I used pytest's tmp_path functionality to create a dummy CSV file. This let me test the reading/writing functionality of the LeaderboardManager's methods without affecting the real leaderboard file.

```python
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
```

### StringInputChecker
I chose a complex regex to use for these tests. It ensures the first chracter is a capital letter, then subsequent characters aren't any of the special characters I listed. I can allow a far more diverse range of inputs by specifying what to exclude instead of include, but certain names will unfortunately still be invalid.

```python
from quiz_utils import StringInputChecker
import pytest

@pytest.fixture(scope="module")
def name_checker():
    return StringInputChecker(max_len=50, format_regex=r"[A-Z][^1-9`¬!?\"£$%^&*()_+={}[\];:@#~|\\,<>\/]*")

def test_empty_name(name_checker):
    assert not name_checker.presence_check("")
    assert not name_checker.presence_check("    ")

def test_names_with_chars(name_checker):
    assert name_checker.format_check("Anne-Marie")
    assert name_checker.format_check("Françoise")
    assert name_checker.format_check("Thomas O'Malley")
    assert not name_checker.format_check(".")
    assert not name_checker.format_check("1337 H@x0r")
    assert not name_checker.format_check("0liver")

def test_name_lengths(name_checker):
    assert name_checker.length_check("Maria Euphonia Demetria Alexandra Jeanette Susanne")
    assert not name_checker.length_check("Suigyō-matsu Unrai-matsu Fūrai-matsu Kū-Neru Tokoro")
```

## Manual testing of the interface
Testing of the streamlit interface was far more informal due to time constraints. During development, I ran through the quiz many times to ensure names and answers were properly checked, widgets generated as they should and the leaderboard was properly written to. To quickly test question types that required higher scores, I changed the code to initialize a user with a higher score.

<img width="1496" height="803" alt="The app rejecting a blank name input." src="https://github.com/user-attachments/assets/b9a00374-3253-492b-a4c1-f25646a20040" />
<img width="1810" height="823" alt="The app rejecting an input of "Li1y" because it contains a number." src="https://github.com/user-attachments/assets/1859f216-990a-4d65-b828-c095bff4e3e6" />
<img width="1282" height="692" alt="The app recognising and celebrating a correct answer." src="https://github.com/user-attachments/assets/bb7b49ce-6334-4b1a-80f3-eb064e91a8f5" />
<img width="1056" height="540" alt="The app rejecting an incorrect answer." src="https://github.com/user-attachments/assets/d8c6a798-95f2-4174-b143-06d520826a4f" />
<img width="888" height="399" alt="The app displaying the "Finish Quiz" button after the user lost all their lives." src="https://github.com/user-attachments/assets/26c27b81-6c0c-4bc8-b3ae-5b4e2659e788" />
<img width="897" height="775" alt="The app displaying its end screen, with the user now on the leaderboard." src="https://github.com/user-attachments/assets/478d7c9c-1f5f-4f49-b8c7-7c7e25f9c8f2" />

# Evaluation
This is an improvement on the previous version. Breaking down the classes and their methods made my code easier to both write and test. Running unit tests for all backend classes gave me confidence in my code and assisted in developing effective methods. Outlining requirement priorities helped direct my work and prevent scope creep.

However, the planning phase took far too long. Many questions I answered then could've been better answered during development and testing. I also put too much time and effort into [prematurely optimizing](https://www.geeksforgeeks.org/software-engineering/premature-optimization/) my code. If this project was something critical that couldn't afford to fail, then my approach would be more justified. But for a simple quiz, a more iterative approach is more appropriate.

If I continue this project, I'd like to deploy it to the [Streamlit Community Cloud](https://streamlit.io/cloud). For this, I'd set up external storage for my leaderboard with either [Google Sheets](https://docs.streamlit.io/develop/tutorials/databases/private-gsheet) or [Supabase.](https://docs.streamlit.io/develop/tutorials/databases/supabase)

For future similar projects, I'd like to investigate alternative web development libraries for python. The things that make it easy to use for simple applications become a hiderance for more complex projects. While it requires more HTML, CSS and JavaScript knowledge, [Flask](https://flask.palletsprojects.com/en/stable/) gives you complete control over the webpage. [Shiny for python](https://shiny.posit.co/py/), a version of the popular R package, also looks promising. It provides more flexibility than streamlit, but appears less complex than Flask.
