import streamlit as st
import sqlite3
from database.db import conn, cursor

st.title("📝 Register")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Register"):

    if username.strip() == "" or password.strip() == "":
        st.warning("Please fill all fields")

    else:
        try:
            cursor.execute(
                """
                INSERT INTO users (username, password)
                VALUES (?, ?)
                """,
                (username, password)
            )

            conn.commit()

            st.success("✅ User registered successfully")

            # Redirect to login page
            st.switch_page("pages/login.py")

            # Stop further execution
            st.stop()

        except sqlite3.IntegrityError:
            st.error("❌ Username already exists")