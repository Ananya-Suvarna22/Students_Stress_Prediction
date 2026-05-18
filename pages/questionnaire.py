import streamlit as st

def run():

    st.title("📝 Student Stress Questionnaire")
    st.markdown("### Analyze student stress based on lifestyle patterns")

    # ---------------- LOGIN CHECK ----------------
    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("⚠ Please login first")
        st.stop()

    # ---------------- ONE-TIME CHECK ----------------
    if st.session_state.get("questionnaire_done", False):
        st.info("ℹ Questionnaire already completed. Please logout/login to retry.")
        st.stop()

    st.divider()

    st.subheader("📊 Enter Your Details")

    # ---------------- INPUT SECTION ----------------
    col1, col2 = st.columns(2)

    with col1:
        sleep = st.slider("😴 Sleep Hours", 0, 12, 6)
        study = st.slider("📚 Study Hours", 0, 15, 5)
        social = st.slider("👥 Social Interaction", 0, 10, 5)

    with col2:
        pressure = st.slider("📉 Academic Pressure", 0, 10, 5)
        attendance = st.slider("🏫 Attendance (%)", 0, 100, 75)
        assignments = st.slider("📝 Assignment Load", 0, 10, 5)

    st.divider()

    # ---------------- ANALYZE BUTTON ----------------
    if st.button("🚀 Analyze Stress Level"):

        # ---------------- FEATURE ENGINEERING ----------------
        score = (
            pressure +
            assignments +
            study -
            sleep -
            social
        )

        # Normalize idea (for better ML feel)
        normalized_score = score / 10

        # ---------------- CLASSIFICATION ----------------
        if score < 10:
            ml_prediction = 0
            label = "Low"
            emoji = "😊"
            color = "success"

        elif score < 20:
            ml_prediction = 1
            label = "Medium"
            emoji = "😐"
            color = "warning"

        else:
            ml_prediction = 2
            label = "High"
            emoji = "😟"
            color = "error"

        # ---------------- RESULT UI ----------------
        st.subheader("🧠 Analysis Result")

        if color == "success":
            st.success(f"{emoji} LOW STRESS DETECTED")
        elif color == "warning":
            st.warning(f"{emoji} MEDIUM STRESS DETECTED")
        else:
            st.error(f"{emoji} HIGH STRESS DETECTED")

        # ---------------- MODEL OUTPUT PANEL ----------------
        st.markdown("### 📊 Feature Breakdown")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Raw Score", score)

        with col2:
            st.metric("Normalized Score", round(normalized_score, 2))

        with col3:
            st.metric("Stress Level", label)

        # ---------------- SAVE TO SESSION ----------------
        st.session_state["ml_prediction"] = ml_prediction
        st.session_state["questionnaire_done"] = True

        st.success("✅ Questionnaire analysis saved successfully")

        # ---------------- INFO ----------------
        st.info("👉 You can now proceed to Face Analysis for hybrid prediction")