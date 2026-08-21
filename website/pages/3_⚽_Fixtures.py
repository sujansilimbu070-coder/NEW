import streamlit as st

from utils.fixture_manager_postgres import get_group_fixtures
from utils.tournament_manager_postgres import get_active_tournament

st.set_page_config(
    page_title="Fixtures",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Fixtures")

# ------------------------------------
# Active Tournament
# ------------------------------------

tournament = get_active_tournament()

if tournament is None:
    st.warning("No active tournament selected.")
    st.stop()

# ------------------------------------
# Tournament Header
# ------------------------------------

st.header(f"🏆 {tournament['tournament_name']}")
st.caption("Official Match Fixtures")

st.divider()

# ------------------------------------
# Load Fixtures
# ------------------------------------

fixtures = get_group_fixtures(tournament["id"])

# ------------------------------------
# No Fixtures
# ------------------------------------

if not fixtures:
    st.info("Fixtures have not been generated yet.")
    st.stop()

current_group = None

for fixture in fixtures:

    # -----------------------------
    # Group Header
    # -----------------------------

    if current_group != fixture["group_name"]:

        current_group = fixture["group_name"]

        st.subheader(f"🏆 {current_group}")

        st.divider()

    # -----------------------------
    # Match Card
    # -----------------------------

    with st.container(border=True):

        st.markdown(f"### ⚽ Match {fixture['match_no']}")

        col1, col2, col3 = st.columns([4, 2, 4])

        with col1:
            st.markdown(
                f"<h4 style='text-align:center'>{fixture['home_team']}</h4>",
                unsafe_allow_html=True
            )

        with col2:

            if fixture["match_status"] == "Played":

                st.markdown(
                    f"<h3 style='text-align:center'>{fixture['home_score']} - {fixture['away_score']}</h3>",
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    "<h3 style='text-align:center'>VS</h3>",
                    unsafe_allow_html=True
                )

        with col3:
            st.markdown(
                f"<h4 style='text-align:center'>{fixture['away_team']}</h4>",
                unsafe_allow_html=True
            )

        st.divider()

        schedule = fixture["match_datetime"]

        if schedule:

            st.write(
            f"📅 {schedule.strftime('%d %b %Y')}"
        )

            st.write(
            f"🕔 {schedule.strftime('%I:%M %p')}"
        )

        else:

            st.write("📅 --")

            st.write("🕔 --")

        if fixture["match_status"] == "Played":

            st.success("🟢 Played")

        else:

            st.warning("🟡 Pending")