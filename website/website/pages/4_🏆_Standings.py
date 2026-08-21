import streamlit as st

from utils.tournament_manager_postgres import get_active_tournament
from utils.standings_manager_postgres import get_group_standings

st.set_page_config(
    page_title="Standings",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Standings")

tournament = get_active_tournament()

if tournament is None:
    st.warning("No active tournament selected.")
    st.stop()

st.header(f"🏆 {tournament['tournament_name']}")
st.caption("Official Group Standings")

st.divider()

standings = get_group_standings(tournament["id"])

if not standings:
    st.info("Standings are not available.")
    st.stop()

group_names = list(standings.keys())

for i in range(0, len(group_names), 2):

    col1, col2 = st.columns(2)

    # -----------------------
    # Left Group
    # -----------------------

    with col1:

        group = group_names[i]

        st.subheader(f"🏆 {group}")

        st.dataframe(
            standings[group],
            use_container_width=True,
            hide_index=True
        )

    # -----------------------
    # Right Group
    # -----------------------

    if i + 1 < len(group_names):

        with col2:

            group = group_names[i + 1]

            st.subheader(f"🏆 {group}")

            st.dataframe(
                standings[group],
                use_container_width=True,
                hide_index=True
            )