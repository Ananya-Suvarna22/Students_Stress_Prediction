import streamlit as st

st.title("📝 Student Stress Questionnaire")

# ---------------- LOGIN CHECK ----------------

if "user" not in st.session_state:

    st.warning("Please login first")

    st.stop()

# ---------------- ONE TIME SUBMISSION CHECK ----------------

if st.session_state.get(
    "questionnaire_done",
    False
):

    st.warning(
        "Questionnaire already submitted. Please relogin."
    )

    st.stop()

# ---------------- INPUTS ----------------

sleep = st.slider(
    "Sleep Hours",
    0,
    12,
    6
)

study = st.slider(
    "Study Hours",
    0,
    15,
    5
)

social = st.slider(
    "Social Interaction",
    0,
    10,
    5
)

pressure = st.slider(
    "Academic Pressure",
    0,
    10,
    5
)

attendance = st.slider(
    "Attendance Percentage",
    0,
    100,
    75
)

assignments = st.slider(
    "Assignment Load",
    0,
    10,
    5
)

# ---------------- ML STRESS LOGIC ----------------

if st.button("Analyze Questionnaire"):

    score = (
        pressure
        + assignments
        + study
        - sleep
        - social
    )

    # ---------------- LOW ----------------

    if score < 10:

        ml_prediction = 0

        st.success(
            "😊 Low Stress from Questionnaire"
        )

    # ---------------- MEDIUM ----------------

    elif score < 20:

        ml_prediction = 1

        st.warning(
            "😐 Medium Stress from Questionnaire"
        )

    # ---------------- HIGH ----------------

    else:

        ml_prediction = 2

        st.error(
            "😟 High Stress from Questionnaire"
        )

    # ---------------- SAVE ML PREDICTION ----------------

    st.session_state[
        "ml_prediction"
    ] = ml_prediction

    # ---------------- LOCK QUESTIONNAIRE ----------------

    st.session_state[
        "questionnaire_done"
    ] = True

    st.success(
        "Questionnaire analysis saved"
    )