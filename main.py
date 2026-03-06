import quiz_utils as q # quiz helper classes
import streamlit as st # for the app interface
from random import shuffle # for shuffling the options list

def start_new_q():
    """Updates session states for the current question, question number and alternate answers."""
    st.session_state.q_num += 1
    st.session_state.current_q = st.session_state.q_gen.gen_random_q()
    alt_q_opts = st.session_state.q_gen.gen_alt_options(st.session_state.current_q, total_q_optns = 4)
    st.session_state.current_q_opts = alt_q_opts + st.session_state.current_q.get_valid_answers()
    shuffle(st.session_state.current_q_opts)
    st.session_state.app_state = "q_ask"
    st.rerun()

def render_name_form(app_state: str, name_checker: q.StringInputChecker = None):
    """Dynamically renders the name input/quiz start form based on the given app_state."""
    
    label_dict = {"start_pg": "Start the Quiz!", "end_pg": "Play Again!"}

    if app_state not in label_dict.keys():
        return st.empty()
    else:
        btn_label = label_dict.get(app_state)

    if "current_usr" in st.session_state and st.session_state.get("current_usr") is not None:
        current_name = st.session_state.current_usr.get_name()
    else:
        current_name = None

    with st.form("name_form", enter_to_submit=False, border=False):
        name_input = st.text_input(label="Enter your name...", value=current_name, label_visibility="collapsed", placeholder="Enter your name...")
        submit_btn = st.form_submit_button(label=btn_label)

    if submit_btn:
        if not name_checker.presence_check(name_input):
            st.error("Please enter your name!")
        elif not name_checker.length_check(name_input):
            st.error("That name is too long! Please use something shorter.")
        elif not name_checker.format_check(name_input):
            st.error("This name isn't in a valid format. Please ensure it starts with a capital letter and doesn't contain any special characters.")
        else:
            st.session_state.current_usr = q.User(name=name_input, lives=3, score=0)
            st.session_state.q_gen.reset_used_rows()
            st.session_state.q_num = 0
            start_new_q()

st.set_page_config(page_title="UK Postcode Quiz",layout="wide",page_icon="🏘️")

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
    </style>
    """,
    unsafe_allow_html=True
)

if "q_gen" not in st.session_state:
    st.session_state["q_gen"] = q.QuestionGenerator(q_details=[("What is the postcode area for {postcode_area_name}?", "postcode_area"), ("What is the full name of the postcode area {postcode_area}?", "postcode_area_name")],
                                                    q_data_source_path="postcode_areas.csv")

if "leaderboard_mgr" not in st.session_state:
    st.session_state["leaderboard_mgr"] = q.LeaderboardManager(source_path="leaderboard.csv")

if "name_checker" not in st.session_state:
    st.session_state["name_checker"] = q.StringInputChecker(max_len=50, format_regex=r"[A-Z][^1-9`¬!?\"£$%^&*()_+={}[\];:@#~|\\,<>\/]*")

if "app_state" not in st.session_state:
    st.session_state["app_state"] = "start_pg"

if "q_num" not in st.session_state:
    st.session_state["q_num"] = 0

if "current_q" not in st.session_state:
    st.session_state["current_q"] = None

if "current_q_opts" not in st.session_state:
    st.session_state["q_opts"] = []

col1, col2, col3 = st.columns(spec=[1,2,1])

with col1:
    with st.expander(label="How to play"):
        st.write("""
            Enter your name and press "Start the Quiz!" to start.
            For each question, click on the option you think is correct.
        """)
        st.write("""
            You earn 1 point for each correct answer, and lose 1 life for each incorrect answer.
            You start with 3 lives, and the quiz ends when you lose them all.
        """)
        st.write("""Try and score as many points as you can and make it onto the leaderboard!""")

with col2:
    st.title("UK Postcode Quiz", text_alignment="center")
    if st.session_state.app_state in ["start_pg","end_pg"]:
        st.header("Leaderboard", text_alignment="center")
        st.plotly_chart(st.session_state.leaderboard_mgr.get_leader_chart())
        render_name_form(st.session_state.app_state, st.session_state.name_checker)
    if st.session_state.app_state in ["q_ask","q_correct","q_incorrect"]:
        st.header("Question {}".format(st.session_state.q_num))
        st.subheader(st.session_state.current_q.get_q_text())
        st.write(st.session_state.current_q_opts)
with col3:
    if st.session_state.app_state in ["q_ask","q_correct","q_incorrect"]:
        st.write("Current Score: {}".format(st.session_state.current_usr.get_score()))
        st.write("Lives: {}".format(st.session_state.current_usr.get_lives()))  