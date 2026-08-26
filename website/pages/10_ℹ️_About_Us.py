import streamlit as st


st.set_page_config(
    page_title="About Us",
    page_icon="ℹ️",
    layout="wide"
)

# ==========================================
# About the Platform
# ==========================================

st.header("🇳🇵 About Nepal eFootball Hub")

st.markdown("""
**Nepal eFootball Hub** is a community-driven platform created to
support and promote competitive eFootball in Nepal.

The platform brings tournament information into one place, including
tournament registrations, group draws, fixtures, standings, qualified
teams, knockout stages, top scorers, and tournament champions.

Our goal is to make Nepal's eFootball tournaments more organized,
transparent, competitive, and enjoyable for players and supporters.
""")


st.divider()


# ==========================================
# Founder
# ==========================================

st.header("👨‍💻 Founder & Developer")

col1, col2 = st.columns([1, 2])


with col1:

    st.image(
        "assets/ananta.jpg",
        width=300
    )


with col2:

    st.markdown("""
## Ananta Silimbu

**Founder & Developer — Nepal eFootball Hub**

Nepal eFootball Hub was created to provide Nepali eFootball players
with a dedicated platform for competitive tournaments and tournament
management.

The platform is designed to bring tournament information, player
participation, match results, standings, knockout stages, and
championship history together in one place.

My goal is to continue developing the platform and contribute to the
growth of a stronger and more organized eFootball community in Nepal.
""")


st.divider()


# ==========================================
# Our Vision
# ==========================================

st.header("🎯 Our Vision")

st.markdown("""
Our vision is to help build a stronger competitive eFootball scene in
Nepal by creating more opportunities for players to participate,
compete, improve their skills, and connect with other players.

We want Nepal eFootball Hub to become a trusted platform for Nepali
eFootball tournaments and players.
""")


st.divider()


# ==========================================
# Our Mission
# ==========================================

st.header("🚀 Our Mission")

st.markdown("""
- 🏆 Organize competitive and fair tournaments
- 🎮 Give players opportunities to compete
- 📊 Provide clear tournament information and results
- 🤝 Connect players within the Nepal eFootball community
- 🌱 Support the growth of competitive eFootball in Nepal
""")


st.divider()


# ==========================================
# Developer Message
# ==========================================

st.divider()

st.header("🇳🇵 For the Love of Nepal eFootball")

st.write(
    "This platform is built with the goal of giving Nepali eFootball "
    "players a better place to compete, connect, and grow."
)

st.subheader("🎮 Play • Compete • Improve 🏆")

st.divider()


# ==========================================
# Footer
# ==========================================

st.divider()

st.title("🇳🇵 Nepal eFootball Community 🇳🇵")

st.markdown("🏆 **Nepal eFootball Hub**")
st.markdown("🎮 **Play • Compete • Improve**")

st.caption("❤️ Made for the Nepal eFootball Community")
st.caption("© 2026 Nepal eFootball Hub")