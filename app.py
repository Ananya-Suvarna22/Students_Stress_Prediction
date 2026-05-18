import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Student Stress Detection System",
    page_icon="🎓",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("🎓 Student Stress Detection System")
st.markdown("### AI-based system for predicting and analyzing student stress levels")

st.divider()

# ---------------- SESSION INIT ----------------
if "user" not in st.session_state:
    st.session_state["user"] = None


# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Navigation")

pages = {
    "🔐 Login": "login",
    "📝 Register": "register",
    "🧠 Questionnaire": "questionnaire",
    "📊 Dashboard": "dashboard",
    "👤 Profile": "profile"
}

page = st.sidebar.radio("Go to", list(pages.keys()))


st.sidebar.divider()


# ---------------- USER INFO PANEL ----------------
if st.session_state["user"]:

    st.sidebar.success(f"👋 Logged in as: {st.session_state['user']}")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.session_state["user"] = None
        st.success("Logged out successfully")
        st.rerun()

else:
    st.sidebar.info("🔒 Not logged in")


st.sidebar.divider()


# ---------------- ROUTER FUNCTION ----------------
def load_page(module_name):
    try:
        module = __import__(f"pages.{module_name}", fromlist=["run"])
        module.run()
    except Exception as e:
        st.error(f"Error loading page: {module_name}")
        st.exception(e)


# ---------------- PAGE ROUTING ----------------
selected_page = pages[page]

load_page(selected_page)