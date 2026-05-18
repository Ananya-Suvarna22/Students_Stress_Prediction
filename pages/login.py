import streamlit as st
import bcrypt
from database.db import cursor


def run():

    st.subheader("🔐 Login to Your Account")

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("🚀 Login"):

        if username.strip() == "" or password.strip() == "":
            st.warning("⚠ Please fill all fields")
            return

        try:
            # ---------------- FETCH USER ----------------
            cursor.execute(
                "SELECT password FROM users WHERE username=?",
                (username,)
            )

            result = cursor.fetchone()

            if result is None:
                st.error("❌ Invalid username or password")
                return

            stored_password = result[0]

            # ---------------- BCRYPT CHECK ----------------
            if bcrypt.checkpw(password.encode(), stored_password):

                st.success("✅ Login Successful")

                st.session_state["user"] = username
                st.session_state["questionnaire_done"] = False
                st.session_state["face_done"] = False

                import time
                time.sleep(1)

                st.rerun()

            else:
                st.error("❌ Invalid username or password")

        except Exception as e:
            st.error("⚠ Database error occurred")
            st.exception(e)