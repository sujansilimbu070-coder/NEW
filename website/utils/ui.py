import streamlit as st


def page_header(title, subtitle=""):
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    st.divider()


def section(title):
    st.subheader(title)


def info_box(text):
    st.info(text)


def success_box(text):
    st.success(text)


def warning_box(text):
    st.warning(text)