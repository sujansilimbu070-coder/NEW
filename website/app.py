import streamlit as st


# ==========================================
# PAGE DEFINITIONS
# ==========================================

home = st.Page(
    "pages/1_🏠_Home.py",
    title="Home",
    icon="🏠"
)

efootball_tournament = st.Page(
    "pages/2_🏆_EFootball_Tournament.py",
    title="EFootball Tournament",
    icon="🏆"
)

top_up = st.Page(
    "pages/8_💳_Top_Up.py",
    title="Top Up",
    icon="💳"
)

our_winners = st.Page(
    "pages/9_🏆_Our_Winners.py",
    title="Our Winners",
    icon="🏆"
)

about_us = st.Page(
    "pages/10_ℹ️_About_Us.py",
    title="About Us",
    icon="ℹ️"
)


# ==========================================
# TOURNAMENT SUB-PAGES
# ==========================================

group_draw = st.Page(
    "pages/3_🎲_Group_Draw.py",
    title="Group Draw",
    icon="🎲"
)

fixtures = st.Page(
    "pages/4_⚽_Fixtures.py",
    title="Fixtures",
    icon="⚽"
)

standings = st.Page(
    "pages/5_🏆_Standings.py",
    title="Standings",
    icon="🏆"
)

qualified_teams = st.Page(
    "pages/6_✅_Qualified_Teams.py",
    title="Qualified Teams",
    icon="✅"
)

knockout = st.Page(
    "pages/7_🏟️_Knockout.py",
    title="Knockout",
    icon="🏟️"
)

top_scorers = st.Page(
    "pages/🏅_Top_Scorers.py",
    title="Top Scorers",
    icon="🏅"
)


# ==========================================
# REGISTER ALL PAGES
# ==========================================

pg = st.navigation(
    [
        home,
        efootball_tournament,
        top_up,
        our_winners,
        about_us,

        # Hidden from sidebar
        group_draw,
        fixtures,
        standings,
        qualified_teams,
        knockout,
        top_scorers,
    ],
    position="hidden"
)


# ==========================================
# SIDEBAR CSS
# ==========================================

st.markdown("""
<style>

/* Remove Streamlit's large sidebar header area */
[data-testid="stSidebarHeader"] {
    display: none !important;
}

/* Remove unnecessary top spacing */
[data-testid="stSidebarContent"] {
    padding-top: 0 !important;
}

/* Remove extra spacing from sidebar content */
[data-testid="stSidebarUserContent"] {
    padding-top: 0 !important;
}

/* Make sidebar content start at the top */
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# CUSTOM SIDEBAR
# ==========================================

with st.sidebar:

    # Website name
    st.markdown(
        """
        <div style="
            font-size:20px;
            font-weight:700;
            padding:15px 5px 12px 5px;
            margin-bottom:8px;
        ">
            🇳🇵 Nepal eFootball Hub
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # Home
    st.page_link(
        home,
        label="Home",
        icon="🏠"
    )

    # EFootball Tournament
    st.page_link(
        efootball_tournament,
        label="EFootball Tournament",
        icon="🏆"
    )

    # Top Up
    st.page_link(
        top_up,
        label="Top Up",
        icon="💳"
    )

    # Our Winners
    st.page_link(
        our_winners,
        label="Our Winners",
        icon="🏆"
    )
    # About Us
    st.page_link(
    about_us,
    label="About Us",
    icon="ℹ️"
)


# ==========================================
# RUN PAGE
# ==========================================

pg.run()