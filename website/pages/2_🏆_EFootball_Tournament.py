import streamlit as st

st.set_page_config(
    page_title="eFootball Tournament",
    page_icon="🏆",
    layout="wide"
)

# ==========================================
# Tournament Header
# ==========================================

st.title("🏆 EFOOTBALL TOURNAMENT")

st.subheader("EFOOTBALL TOURNAMENT SEASON 2")

st.caption("Official Nepal eFootball Tournament Platform")

st.divider()


# ==========================================
# Tournament Navigation
# ==========================================

st.header("🏆 Tournament")

st.write("Select a section below to view the tournament information.")


# ==========================================
# Row 1
# ==========================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🎲 Group Draw")
    st.write("View all tournament groups and participating players.")

    if st.button("Open Group Draw", use_container_width=True):
        st.switch_page("pages/3_🎲_Group_Draw.py")


with col2:
    st.subheader("⚽ Fixtures")
    st.write("View all upcoming and completed tournament matches.")

    if st.button("Open Fixtures", use_container_width=True):
        st.switch_page("pages/4_⚽_Fixtures.py")


st.divider()


# ==========================================
# Row 2
# ==========================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Standings")
    st.write("Check group standings, points, goals and rankings.")

    if st.button("Open Standings", use_container_width=True):
        st.switch_page("pages/5_🏆_Standings.py")


with col2:
    st.subheader("✅ Qualified Teams")
    st.write("View teams that qualified for the knockout stage.")

    if st.button("Open Qualified Teams", use_container_width=True):
        st.switch_page("pages/6_✅_Qualified_Teams.py")


st.divider()


# ==========================================
# Row 3
# ==========================================

st.subheader("🏟️ Knockout Stage")

st.write(
    "Follow the knockout stage, quarter-finals, "
    "semi-finals and final."
)

if st.button("Open Knockout", use_container_width=True):
    st.switch_page("pages/7_🏟️_Knockout.py")


st.divider()

st.divider()

# ==========================================
# Top Scorers
# ==========================================

st.subheader("🏅 Top Scorers")

st.write(
    "View the leading goal scorers of the tournament."
)

if st.button("Open Top Scorers", use_container_width=True):
    st.switch_page("pages/🏅_Top_Scorers.py")

# ==========================================
# Tournament Information
# ==========================================

st.header("🇳🇵 Nepal eFootball")

st.write(
    "Follow the complete Nepal eFootball Tournament "
    "from the group stage to the final."
)

st.caption(
    "🏆 Group Draw  •  ⚽ Fixtures  •  🏆 Standings  •  "
    "✅ Qualified Teams  •  🏟️ Knockout"
)

st.divider()

