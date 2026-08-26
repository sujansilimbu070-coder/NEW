import streamlit as st

from utils.tournament_manager_postgres import get_active_tournament
from utils.group_manager_postgres import get_group_teams

st.set_page_config(
    page_title="Group Draw",
    page_icon="🎲",
    layout="wide"
)

st.title("🎲 Group Draw")

# -----------------------------
# Check Tournament
# -----------------------------
tournament = get_active_tournament()

if tournament is None:
    st.warning("No active tournament selected.")
    st.stop()

# -----------------------------
# Read Groups
# -----------------------------

group_teams = get_group_teams(tournament["id"])

st.header(f"🏆 {tournament['tournament_name']}")
st.caption("Official Group Draw")

st.divider()

group_names = list(group_teams.keys())

for i in range(0, len(group_names), 2):

    col1, col2 = st.columns(2)

    # -------------------------
    # Left Group
    # -------------------------

    with col1:

        group = group_names[i]

        with st.container(border=True):

            st.subheader(f"🏆 {group}")

            st.divider()

            for team in group_teams[group]:
                st.write(f"🔹 {team['team_name']}")

    # -------------------------
    # Right Group
    # -------------------------

    if i + 1 < len(group_names):

        with col2:

            group = group_names[i + 1]

            with st.container(border=True):

                st.subheader(f"🏆 {group}")

                st.divider()

                for team in group_teams[group]:
                    st.write(f"🔹 {team['team_name']}")