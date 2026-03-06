import quiz_utils as q  # quiz helper classes
import streamlit as st  # for the app interface
from random import shuffle  # for shuffling the options list


# procedures for updating session states
def check_answer_and_update():
    """Checks the selected answer, updates the user's score/lives and the app's state accordingly."""
    a_to_check = st.session_state.selected_a
    if a_to_check is None:
        pass
    elif st.session_state.current_q.check_answer(a_to_check):
        st.session_state.current_usr.add_score(1)
        st.balloons()
        st.session_state.app_state = "q_correct"
    else:
        st.session_state.current_usr.lose_lives(1)
        st.session_state.app_state = "q_incorrect"


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


def check_name_start_quiz():
    """
    Checks if the user has input a valid name. If it's valid, the quiz starts.
    If it isn't, the relevant error is displayed.
    """
    name_checker = st.session_state.name_checker
    name_input = st.session_state.usr_name_input

    if not name_checker.presence_check(name_input):
        st.error("Please enter your name!")
    elif not name_checker.length_check(name_input):
        st.error("That name is too long! Please use something shorter.")
    elif not name_checker.format_check(name_input):
        st.error(
            "This name isn't in a valid format. Please ensure it starts with a capital letter and doesn't contain any special characters."
        )
    else:
        st.session_state.current_usr = q.User(name=name_input, lives=3, score=0)
        st.session_state.q_gen.reset_used_rows()
        st.session_state.q_num = 0
        start_new_q()


def save_results_end_quiz():
    """
    Saves the current user's results, clears the user's details,
    then changes the session state to the end page.
    """
    st.session_state.leaderboard_mgr.save_result_and_update(
        user_to_add=st.session_state.current_usr
    )
    st.session_state.prev_usr_name = st.session_state.current_usr.get_name()
    st.session_state.prev_usr_score = st.session_state.current_usr.get_score()
    st.session_state.current_usr = None
    st.session_state.app_state = "end_pg"


# procedures for rendering widgets
def render_name_form():
    """
    Dynamically renders the name input/quiz start form based on the current app_state.
    When the button is clicked, it will validate the given input and start the quiz if a valid name was given.
    """

    app_state = st.session_state.app_state

    label_dict = {"start_pg": "Start the Quiz!", "end_pg": "Play Again!"}

    if app_state not in label_dict.keys():
        return st.empty()
    else:
        btn_label = label_dict.get(app_state)

    if st.session_state.prev_usr_name is not None:
        prev_name = st.session_state.prev_usr_name
    else:
        prev_name = None

    with st.form("name_form", enter_to_submit=False, border=False):
        st.text_input(
            label="Enter your name...",
            value=prev_name,
            label_visibility="collapsed",
            placeholder="Enter your name...",
            key="usr_name_input",
        )
        st.form_submit_button(label=btn_label, on_click=check_name_start_quiz)


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


def render_result_msg():
    """Renders the result text based on the app's current state."""
    app_state = st.session_state.app_state
    if app_state == "q_correct":
        st.write("Correct! Well done!")
    elif app_state == "q_incorrect":
        st.write(
            "Incorrect! The answer was {}.".format(
                st.session_state.current_q.get_valid_answers()[0]
            )
        )
    else:
        return st.empty()


def render_next_btn():
    """
    Renders either the "Next Question" or "Finish Quiz" button,
    depending on how many lives the current user has left.
    """
    if st.session_state.current_usr.get_lives() == 0:
        st.button(label="Finish Quiz", on_click=save_results_end_quiz())
    else:
        st.button(label="Next Question", on_click=start_new_q())


st.set_page_config(page_title="UK Postcode Quiz", layout="wide", page_icon="🏘️")

# custom CSS for colouring uncooperative widgets
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

if "q_gen" not in st.session_state:
    st.session_state["q_gen"] = q.QuestionGenerator(
        q_details=[
            ("What is the postcode area for {postcode_area_name}?", "postcode_area"),
            (
                "What is the full name of the postcode area {postcode_area}?",
                "postcode_area_name",
            ),
        ],
        q_data_source_path="postcode_areas.csv",
    )

if "leaderboard_mgr" not in st.session_state:
    st.session_state["leaderboard_mgr"] = q.LeaderboardManager(
        source_path="leaderboard.csv", board_size=3
    )

if "name_checker" not in st.session_state:
    st.session_state["name_checker"] = q.StringInputChecker(
        max_len=50, format_regex=r"[A-Z][^1-9`¬!?\"£$%^&*()_+={}[\];:@#~|\\,<>\/]*"
    )

if "app_state" not in st.session_state:
    st.session_state["app_state"] = "start_pg"

if "q_num" not in st.session_state:
    st.session_state["q_num"] = 0

if "current_q" not in st.session_state:
    st.session_state["current_q"] = None

if "current_q_opts" not in st.session_state:
    st.session_state["current_q_opts"] = []

if "prev_usr_name" not in st.session_state:
    st.session_state["prev_usr_name"] = None

if "prev_usr_score" not in st.session_state:
    st.session_state["prev_usr_Score"] = None

if "current_q_type" not in st.session_state:
    st.session_state["current_q_type"] = "selectbox"

# reset selected answer when a new question is generated
if st.session_state.app_state == "q_ask":
    st.session_state.selected_a = None

col1, col2, col3 = st.columns(spec=[1, 2, 1])

with col1:
    with st.expander(label="How to play"):
        st.write("""
            Enter your name and press "Start the Quiz!" to start.
            For each question, select the option you think is correct.
        """)
        st.write("""
            You earn 1 point for each correct answer, and lose 1 life for each incorrect answer.
            You start with 3 lives, and the quiz ends when you lose them all.
        """)
        st.write(
            """Try and score as many points as you can and make it onto the leaderboard!"""
        )

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
with col3:
    if st.session_state.app_state in ["q_ask", "q_correct", "q_incorrect"]:
        st.write(
            "Current Score: {}\n\nLives: {}".format(
                st.session_state.current_usr.get_score(),
                st.session_state.current_usr.get_lives(),
            )
        )
