import streamlit as st
import urllib.parse

st.set_page_config(
    page_title="eFootball Top Up",
    page_icon="💳",
    layout="wide"
)

# ==========================================
# PAGE TITLE
# ==========================================

st.title("💳 eFootball Top Up")

st.subheader("🇳🇵 Nepal eFootball Hub")

st.write(
    "Enter your details below and send your top-up request directly "
    "to Sudip Limbu on WhatsApp."
)

st.divider()


# ==========================================
# PLAYER INFORMATION
# ==========================================

st.header("👤 Player Information")

player_name = st.text_input(
    "Your Name",
    placeholder="Enter your name"
)

player_id = st.text_input(
    "eFootball User ID",
    placeholder="Enter your eFootball User ID"
)


# ==========================================
# TOP UP PACKAGE
# ==========================================

st.header("💰 Select Top Up Package")

package = st.selectbox(
    "Choose your package",
    [
        "Select Package",
        "100 eFootball Coins",
        "250 eFootball Coins",
        "500 eFootball Coins",
        "1,000 eFootball Coins",
        "2,000 eFootball Coins",
        "Other / Custom Package"
    ]
)


# ==========================================
# SEND TO WHATSAPP
# ==========================================

st.divider()

if st.button("💬 Send Top-Up Request on WhatsApp", type="primary"):

    if not player_name.strip():
        st.error("Please enter your name.")

    elif not player_id.strip():
        st.error("Please enter your eFootball User ID.")

    elif package == "Select Package":
        st.error("Please select a top-up package.")

    else:

        message = (
            "Hello Sudip Limbu 👋\n\n"
            "I want to purchase an eFootball top-up.\n\n"
            f"👤 Name: {player_name}\n"
            f"🎮 eFootball User ID: {player_id}\n"
            f"💰 Package: {package}\n\n"
            "Please provide the payment details. Thank you! 🙏"
        )

        encoded_message = urllib.parse.quote(message)

        whatsapp_url = (
            "https://wa.me/8201021921163"
            f"?text={encoded_message}"
        )

        st.success("Your request is ready!")

        st.link_button(
            "📲 Open WhatsApp & Send Request",
            whatsapp_url
        )

        st.info(
            "WhatsApp will open with your message already prepared. "
            "Please check the details and press Send."
        )


# ==========================================
# DIRECT WHATSAPP CONTACT
# ==========================================

st.divider()

st.subheader("📱 Contact Sudip Limbu")

st.link_button(
    "💬 WhatsApp Sudip Limbu",
    "https://wa.me/8201021921163"
)

# ==========================================
# CONTACT
# ==========================================

st.divider()

st.subheader("📘 Facebook ")

st.link_button(
    "Open Sudip Limbu Facebook",
    "https://www.facebook.com/sudip.limbu.650069"
)

# ==========================================
# IMPORTANT
# ==========================================

st.divider()

st.subheader("⚠️ Important")

st.write(
    "• Double-check your eFootball User ID before sending."
)

st.write(
    "• Never share your eFootball account password."
)

st.write(
    "• Confirm the package and payment amount with Sudip before paying."
)


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.write("🇳🇵 Nepal eFootball Community 🇳🇵")

st.caption("Powered by Nepal eFootball Hub")