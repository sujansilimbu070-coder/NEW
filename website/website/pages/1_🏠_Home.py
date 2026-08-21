import streamlit as st
from utils.tournament_manager_postgres import get_active_tournament
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
from pathlib import Path

css_file = Path(__file__).parent.parent / "assets" / "styles.css"

with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    active_tournament = get_active_tournament()
# -----------------------------
# HERO
# -----------------------------

st.markdown("""
<div class="hero">

<h1>🏆</h1>

<h1>Nepal efootball Hub</h1>

<h3>The Home of Competitive eFootball in Nepal</h3>

<p>
Welcome to the official platform of Nepal eFootball Hub.
Explore tournaments, fixtures, standings, knockout stages,
and championship history—all in one place.
</p>

</div>
""", unsafe_allow_html=True)

st.divider()

#-----------------------------
# Our vission
#-----------------------------
st.divider()

st.header("🌍 Our Vision")

st.markdown("""
Nepal eFootball Hub envisions becoming the leading competitive eFootball platform in Nepal, bringing together passionate players through fair, exciting, and professionally organized tournaments.

Our mission is to create opportunities for every player to compete, improve their skills, connect with the gaming community, and contribute to the growth of eFootball in Nepal.

Together, we are building a stronger, more united future for Nepal's eFootball community.
""")

# -----------------------------
# About
# -----------------------------

st.divider()

st.header("🇳🇵 About Nepal eFootball Hub")

st.markdown("""
Nepal eFootball Hub is a community-driven platform dedicated to promoting
competitive eFootball across Nepal.

Our mission is to organize fair, exciting, and professional tournaments
that bring together passionate players from all over the country.

Whether you're competing for the championship or following your favorite
players, Nepal eFootball Hub is your destination for fixtures, standings,
knockout stages, and tournament updates.
""")

# -----------------------------
# Meet Our Team
# -----------------------------

st.divider()

st.header("👨‍💻 Founder & Developer")

col1, col2 = st.columns([1,2])

with col1:
    st.image("assets/ananta.jpg", width=350)

with col2:
    st.markdown("""
# Ananta Silimbu

Founder & Developer of Nepal eFootball Hub.

This platform was created to provide Nepali eFootball players with
a professional tournament experience through live fixtures,
standings, knockout stages, and championship tracking.

**"Building the future of Nepal eFootball, one tournament at a time."**
""")