import streamlit as st
from pathlib import Path
from components.match_card import match_card
from utils.tournament_manager_postgres import get_active_tournament
from utils.knockout_manager_postgres import get_knockout_fixtures
from utils.fixture_manager_postgres import is_group_stage_complete

st.set_page_config(
    page_title="Knockout",
    page_icon="🏟️",
    layout="wide"
)

css_file = Path(__file__).parent.parent / "assets" / "knockout.css"

with open(css_file) as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.title("🏟️ Knockout")

tournament = get_active_tournament()

if tournament is None:
    st.warning("No active tournament selected.")
    st.stop()

# ==========================================
# Check Group Stage Completion
# ==========================================

if not is_group_stage_complete(tournament["id"]):

    st.warning("""
⚠️ The Group Stage is still in progress.

Complete all group matches before viewing the knockout bracket.
""")

    st.stop()


st.header(f"🏆 {tournament['tournament_name']}")
st.caption("Official Knockout Bracket")

st.divider()

matches = get_knockout_fixtures(
    tournament["id"]
)

if not matches:
    st.info("Knockout has not been generated yet.")
    st.stop()

# ----------------------------------------
# Separate Matches by Stage
# ----------------------------------------

round16 = [m for m in matches if m["stage"] == "Round of 16"]
quarter = [m for m in matches if m["stage"] == "Quarter Final"]
semi = [m for m in matches if m["stage"] == "Semi Final"]
final = [m for m in matches if m["stage"] == "Final"]

# ----------------------------------------
# Create 4 Columns
# ----------------------------------------

col1, col2, col3, col4, col5 = st.columns([3, 3, 3, 3, 2])

# ---------------- Round of 16 ----------------

with col1:

    st.subheader("Round of 16")

    for match in round16:
        match_card(match)

# ---------------- Quarter Final ----------------

with col2:

    st.subheader("Quarter Final")

    if quarter:

        for match in quarter:
            match_card(match)

    else:
        st.empty()

# ---------------- Semi Final ----------------

with col3:

    st.subheader("Semi Final")

    if semi:

        for match in semi:
            match_card(match)

    else:
        st.empty()

# ---------------- Final ----------------

with col4:

    st.subheader("Final")

    if final:

        for match in final:
            match_card(match)

    else:
        st.empty()

        # ---------------- Champion ----------------

from utils.knockout_manager_postgres import get_champion

with col5:

    st.subheader("🏆 Champion")

    champion = get_champion(
        tournament["id"]
    )

    for _ in range(8):
        st.write("")

    with st.container(border=True):

        if champion:

            st.markdown(
                f"""
                <div style="text-align:center">
                    <h1>🏆</h1>
                    <h2>{champion}</h2>
                    <p>Champion</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div style="text-align:center">
                    <h1>🏆</h1>
                    <h3>To Be Decided</h3>
                </div>
                """,
                unsafe_allow_html=True
            )