import streamlit as st
from utils.fixture_manager_postgres import get_top_scorers
from utils.tournament_manager_postgres import get_active_tournament
from utils.fixture_manager_postgres import get_top_scorers

tournament = get_active_tournament()

scorers = get_top_scorers(tournament["id"])

st.title("🏅 Top Scorers")

for i, player in enumerate(scorers, start=1):

    if i == 1:
        medal = "🥇"
    elif i == 2:
        medal = "🥈"
    elif i == 3:
        medal = "🥉"
    else:
        medal = f"{i}."

    st.write(f"{medal} **{player['team_name']}** — ⚽ {player['goals']} Goals")