import streamlit as st
from database.db import cursor

st.title("🔐 Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    if user:
        st.success("Login Successful")

        st.session_state["user"] = username

        st.session_state["questionnaire_done"] = False

        st.session_state["face_done"] = False

    else:
        st.error("Invalid Username or Password")