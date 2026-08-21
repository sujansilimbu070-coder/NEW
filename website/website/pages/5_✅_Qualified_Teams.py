from utils.fixture_manager_postgres import is_group_stage_complete
import streamlit as st

from utils.tournament_manager_postgres import (
    get_active_tournament,
    get_tournament_status,
)

from utils.qualification_manager_postgres import get_qualified_teams


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Qualified Teams",
    page_icon="✅",
    layout="wide"
)

st.title("✅ Qualified Teams")


# ==========================================
# Active Tournament
# ==========================================

tournament = get_active_tournament()

if tournament is None:
    st.warning("No active tournament selected.")
    st.stop()

# ==========================================
# Tournament Status Check
# ==========================================

from utils.fixture_manager_postgres import is_group_stage_complete

if not is_group_stage_complete(tournament["id"]):

    st.warning(
        "⚠️ The Group Stage is still in progress.\n\nComplete all group matches before viewing the qualified teams."
    )

    st.stop()

# ==========================================
# Header
# ==========================================

st.header(f"🏆 {tournament['tournament_name']}")
st.caption("Teams Qualified for Knockout Stage")

st.divider()


# ==========================================
# Load Qualified Teams
# ==========================================

qualified = get_qualified_teams(
    tournament["id"]
)

if not qualified:

    st.info("No teams have qualified yet.")

    st.stop()


# ==========================================
# Display Qualified Teams
# ==========================================

current_group = None

for team in qualified:

    # --------------------------------------
    # Group Header
    # --------------------------------------

    if current_group != team["Group"]:

        current_group = team["Group"]

        st.subheader(f"🏆 {current_group}")

        st.divider()

    # --------------------------------------
    # Qualified Team Card
    # --------------------------------------

    with st.container(border=True):

        medal = "🥇" if team["Pos"] == 1 else "🥈"

        st.markdown(
            f"## {medal} {team['Team']}"
        )

        st.caption(
            f"Position {team['Pos']} • {team['Pts']} Points"
        )