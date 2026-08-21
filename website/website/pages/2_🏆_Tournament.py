import streamlit as st

from utils.tournament_manager_postgres import (
    get_active_tournament
)

from utils.fixture_manager_postgres import (
    get_group_fixtures
)

st.set_page_config(
    page_title="Tournament",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Tournament")

# ==========================================
# Active Tournament
# ==========================================

tournament = get_active_tournament()

if tournament is None:

    st.warning("No active tournament.")

    st.stop()

st.success(
    f"Current Tournament : {tournament['tournament_name']}"
)

st.divider()

# ==========================================
# Load Fixtures
# ==========================================

group_fixtures = get_group_fixtures(
    tournament["id"]
)

st.header("🏆 Group Stage")

current_group = None

for fixture in group_fixtures:

    if current_group != fixture["group_name"]:

        current_group = fixture["group_name"]

        st.subheader(current_group)

    st.write(
        f"⚽ Match {fixture['match_no']}"
    )

    # Pending Match
    if fixture["match_status"] == "Pending":

        st.write(
            f"**{fixture['home_team']}**"
        )

        st.write("VS")

        st.write(
            f"**{fixture['away_team']}**"
        )

        st.warning("🟡 Pending")

    # Played Match
    else:

        st.write(
            f"**{fixture['home_team']}**"
        )

        st.write(
            f"### {fixture['home_score']}  -  {fixture['away_score']}"
        )

        st.write(
            f"**{fixture['away_team']}**"
        )

        st.success("🟢 Played")

    st.divider()