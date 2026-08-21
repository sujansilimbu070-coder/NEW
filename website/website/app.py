import streamlit as st
from utils.tournament_manager_postgres import get_active_tournament

st.set_page_config(
    page_title="Nepal eFootball Hub",
    page_icon="🏆",
    layout="wide"
)

# ==========================================
# Active Tournament
# ==========================================

tournament = get_active_tournament()

# ==========================================
# Header
# ==========================================

st.markdown("""
<div style='text-align:center;'>

<h1>🇳🇵 Nepal eFootball Hub 🇳🇵</h1>

<h4 style='color:gray;'>
Official Tournament Platform
</h4>

</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================
# Sponsor Section
# ==========================================

st.markdown("""
<div style="
background:linear-gradient(135deg,#0f172a,#1e293b);
padding:18px;
border-radius:20px;
border:2px solid gold;
text-align:center;
">

<h2 style="color:gold;">
🌟 PROUDLY SPONSORED BY 🌟
</h2>

</div>
""", unsafe_allow_html=True)

st.write("")

col1, col2 = st.columns(2)

# ==========================================
# Sudip Limbu
# ==========================================

with col1:

    st.image(
        "assets/sudip.jpg",
        use_container_width=True
    )

    st.markdown(
        "<h2 style='text-align:center;'>Sudip Limbu</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h4 style='text-align:center;color:#f4b400;'>🇳🇵 Nepal | 🇰🇷 South Korea</h4>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <p style="
        text-align:center;
        font-size:18px;
        color:#444;
        line-height:1.8;
        padding:10px 20px;
    ">
        <i>
        "Proudly supporting the growth of Nepal eFootball
        and inspiring Nepali gamers to compete on a bigger stage."
        </i>
    </p>
    """, unsafe_allow_html=True)

# ==========================================
# Pustam Limbu
# ==========================================

with col2:

    st.image(
        "assets/pustam.jpg",
        use_container_width=True
    )

    st.markdown(
        "<h2 style='text-align:center;'>Pustam Limbu</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h4 style='text-align:center;color:#f4b400;'>🇳🇵 Nepal | 🇰🇷 South Korea</h4>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <p style="
        text-align:center;
        font-size:18px;
        color:#444;
        line-height:1.8;
        padding:10px 20px;
    ">
        <i>
        "Helping build a stronger Nepal eFootball community
        by supporting tournaments and future generations of players."
        </i>
    </p>
    """, unsafe_allow_html=True)

# ==========================================
# Thank You Sponsors
# ==========================================

st.markdown("""
<div style="
text-align:center;
padding:20px;
">

<h2 style="color:#FFD700;">
🙏 Thank You to Our Sponsors
</h2>

<p style="
font-size:18px;
line-height:1.8;
color:#555;
">

We sincerely thank <b>Sudip Limbu</b> and <b>Pustam Limbu</b>
for their generous support and dedication to the Nepal eFootball community.
Your contribution helps us organize tournaments, inspire players,
and continue building a stronger eFootball community in Nepal.

</p>

<h3 style="color:#1565C0;">
🇳🇵 Together, let's grow Nepal eFootball.
</h3>

</div>
""", unsafe_allow_html=True)

st.divider()

st.markdown("""
<div style="text-align:center;color:gray;">

© 2026 Nepal eFootball Hub

Made with ❤️ for the Nepal eFootball Community

</div>
""", unsafe_allow_html=True)