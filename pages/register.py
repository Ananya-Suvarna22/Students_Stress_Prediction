import streamlit as st
import sqlite3
import bcrypt
from database.db import conn, cursor


def run():

    st.subheader("📝 Create New Account")
    st.markdown("Register to access the Student Stress Detection System")

    # ---------------- UI LAYOUT ----------------
    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input("👤 Username")

    with col2:
        password = st.text_input("🔒 Password", type="password")

    confirm_password = st.text_input("🔒 Confirm Password", type="password")

    st.markdown("---")

    # ---------------- REGISTER BUTTON ----------------
    if st.button("🚀 Register"):

        # ---------------- VALIDATION ----------------
        if username.strip() == "" or password.strip() == "":
            st.warning("⚠️ Please fill all fields")
            return

        if password != confirm_password:
            st.error("❌ Passwords do not match")
            return

        if len(password) < 4:
            st.warning("⚠️ Password should be at least 4 characters")
            return

        try:
            # ---------------- CHECK EXISTING USER ----------------
            cursor.execute(
                "SELECT * FROM users WHERE username=?",
                (username,)
            )

            existing_user = cursor.fetchone()

            if existing_user:
                st.error("❌ Username already exists")
                return

            # ---------------- HASH PASSWORD ----------------
            hashed_password = bcrypt.hashpw(
                password.encode(),
                bcrypt.gensalt()
            )

            # ---------------- INSERT USER ----------------
            cursor.execute(
                """
                INSERT INTO users (username, password)
                VALUES (?, ?)
                """,
                (username, hashed_password)
            )

            conn.commit()

            st.success("✅ Registration successful!")

            st.info("👉 Redirecting to login page...")

            import time
            time.sleep(1)

            st.switch_page("pages/login.py")

            st.stop()

        except sqlite3.Error as e:
            st.error("⚠️ Database error occurred")
            st.exception(e)