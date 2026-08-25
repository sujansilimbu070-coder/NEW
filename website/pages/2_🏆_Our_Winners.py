import streamlit as st

st.set_page_config(
    page_title="Tournament Winners",
    page_icon="🏆",
    layout="wide"
)

# ==========================================
# HEADER
# ==========================================

st.title("🏆 NEPAL EFOOTBALL TOURNAMENT")

st.subheader("EFOOTBALL TOURNAMENT SEASON 1")

st.divider()

# ==========================================
# 1ST PLACE
# ==========================================

st.subheader("🥇 1st Place")

col1, col2 = st.columns([1, 2])


with col1:

    st.image(
        "assets/raju.jpg",
        width=180
    )

    st.subheader("Raju Baniya")


with col2:

    st.subheader("🏆 Champion")

    st.write(
        "Congratulations to Raju Baniya for securing "
        "1st place and becoming the champion of the tournament. "
        "A great performance and a well-deserved victory."
    )


st.divider()


# ==========================================
# 2ND PLACE
# ==========================================

st.subheader("🥈 2nd Place")

col1, col2 = st.columns([1, 2])


with col1:

    st.image(
        "assets/madan.jpg",
        width=180
    )

    st.subheader("Madan Tabebung Limbu")


with col2:

    st.subheader("🥈 Runner-up")

    st.write(
        "Congratulations to Madan Tabebung Limbu for an "
        "excellent performance and securing 2nd place "
        "in the tournament."
    )


st.divider()


# ==========================================
# FOOTER
# ==========================================

st.write("🇳🇵 Nepal eFootball Community 🇳🇵")

st.caption("Celebrating our players and champions")