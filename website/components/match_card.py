import streamlit as st


def match_card(match):
    """
    Display one knockout match card.
    """

    with st.container(border=True):

        # ----------------------------
        # Match Title
        # ----------------------------

        st.markdown(f"### ⚽ Match {match['match_no']}")

        # ----------------------------
        # Home Team
        # ----------------------------

        st.markdown(
            f"<h4 style='text-align:center;'>{match['home_team_name']}</h4>",
            unsafe_allow_html=True
        )

        st.markdown("---")

        # ----------------------------
        # Score
        # ----------------------------

        if match["match_status"] == "Played":

            st.markdown(
                f"""
                <h2 style='text-align:center;'>
                    {match['home_score']} - {match['away_score']}
                </h2>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                "<h2 style='text-align:center;'>VS</h2>",
                unsafe_allow_html=True
            )

        st.markdown("---")

        # ----------------------------
        # Away Team
        # ----------------------------

        st.markdown(
            f"<h4 style='text-align:center;'>{match['away_team_name']}</h4>",
            unsafe_allow_html=True
        )

        # ----------------------------
        # Penalty Shootout
        # ----------------------------

        if (
            match["penalty_home"] is not None
            and
            match["penalty_away"] is not None
        ):

            st.markdown("")

            st.markdown(
                "<h5 style='text-align:center;'>🏅 Penalties</h5>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <h3 style='text-align:center;'>
                    {match['penalty_home']} - {match['penalty_away']}
                </h3>
                """,
                unsafe_allow_html=True
            )

        st.markdown("")

        # ----------------------------
        # Match Status
        # ----------------------------
        schedule = match["match_datetime"]
 
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


        if match["match_status"] == "Played":
            st.success("🟢 Played")
        else:
            st.warning("🟡 Pending")