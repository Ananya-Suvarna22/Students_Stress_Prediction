import streamlit as st

st.set_page_config(
    page_title="Stress Detection System",
    layout="wide"
)

st.title("🎓 Student Stress Detection System")

# ---------------- SIDEBAR ----------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Login",
        "Register",
        "Questionnaire",
        "Dashboard",
        "Profile"
    ]
)

# ---------------- LOGOUT BUTTON ----------------

st.sidebar.markdown("---")

if "user" in st.session_state:

    st.sidebar.write(
        f"👋 Welcome {st.session_state['user']}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.clear()

        st.success(
            "Logged out successfully"
        )

        st.rerun()

# ---------------- PAGE ROUTING ----------------

if page == "Login":

    import pages.login

elif page == "Register":

    import pages.register

elif page == "Questionnaire":

    import pages.questionnaire

elif page == "Dashboard":

    import pages.dashboard

elif page == "Profile":

    import pages.profile