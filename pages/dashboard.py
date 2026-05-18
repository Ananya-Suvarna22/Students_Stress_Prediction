import streamlit as st
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils.fusion import hybrid_fusion
from utils.face_detection import detect_face
from utils.prediction import predict_stress
from database.db import conn, cursor
from utils.suggestions import get_suggestion


def run():

    st.title("📊 Stress Analysis Dashboard")
    st.markdown("AI-powered hybrid stress detection system")

    # ---------------- LOGIN CHECK ----------------
    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("⚠ Please login first to access dashboard")
        st.stop()

    username = st.session_state["user"]
    st.success(f"👋 Welcome {username}")

    st.divider()

    # ---------------- STATUS PANEL ----------------
    col1, col2 = st.columns(2)

    with col1:
        if "ml_prediction" in st.session_state:
            st.success("✅ Questionnaire Completed")
        else:
            st.warning("⚠ Questionnaire Pending")

    with col2:
        face_done = st.session_state.get("face_done", False)
        if face_done:
            st.info("📷 Face analysis already done")
        else:
            st.info("📷 Ready for face analysis")

    st.divider()

    # ---------------- CAMERA SECTION ----------------
    st.subheader("📷 Facial Stress Detection")

    camera = st.camera_input("Capture your face")

    if camera is not None:

        file_bytes = np.asarray(bytearray(camera.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)

        face = detect_face(frame)

        if face is None:
            st.error("❌ No face detected. Try again.")
            return

        # ---------------- PREDICTIONS ----------------
        cnn_prediction = predict_stress(face)
        ml_prediction = st.session_state.get("ml_prediction", 1)

        final_stress = hybrid_fusion(ml_prediction, cnn_prediction)

        # ---------------- STORE DATA ----------------
        cursor.execute(
            """
            INSERT INTO stress_data (username, stress_level)
            VALUES (?, ?)
            """,
            (username, final_stress)
        )
        conn.commit()

        st.divider()

        # ---------------- RESULT UI CARD ----------------
        st.subheader("🧠 Final Stress Result")

        if final_stress == "Low":
            st.success("😊 LOW STRESS")
        elif final_stress == "Medium":
            st.warning("😐 MEDIUM STRESS")
        else:
            st.error("😟 HIGH STRESS")

        # ---------------- MODEL BREAKDOWN ----------------
        st.markdown("### 📊 Model Breakdown")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Questionnaire Score", ml_prediction)

        with col2:
            st.metric("CNN Score", cnn_prediction)

        with col3:
            st.metric("Final Result", final_stress)

        # ---------------- SUGGESTIONS ----------------
        st.info("💡 " + get_suggestion(final_stress))

        st.session_state["face_done"] = True

    st.divider()

    # ---------------- HISTORY SECTION ----------------
    st.subheader("📈 Stress History")

    df = pd.read_sql(
        f"""
        SELECT * FROM stress_data
        WHERE username='{username}'
        """,
        conn
    )

    if df.empty:
        st.info("No stress data available yet")
        return

    df["date"] = pd.to_datetime(df["date"])

    # ---------------- FILTER ----------------
    option = st.selectbox(
        "Filter records",
        ["All", "Today", "Last 7 Days"]
    )

    if option == "Today":
        df = df[df["date"].dt.date == pd.Timestamp.today().date()]

    elif option == "Last 7 Days":
        df = df[df["date"] > pd.Timestamp.now() - pd.Timedelta(days=7)]

    st.divider()

    # ---------------- CHARTS ----------------
    st.subheader("📊 Stress Trends")

    stress_numeric = df["stress_level"].map({
        "Low": 1,
        "Medium": 2,
        "High": 3
    })

    st.line_chart(stress_numeric)

    st.subheader("📊 Distribution")

    fig, ax = plt.subplots()

    df["stress_level"].value_counts().plot(
        kind="bar",
        ax=ax
    )

    ax.set_ylabel("Count")
    ax.set_title("Stress Level Distribution")

    st.pyplot(fig)

    # ---------------- PIE CHART ----------------
    st.subheader("🍰 Stress Share")

    fig2, ax2 = plt.subplots()

    df["stress_level"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax2
    )

    ax2.set_ylabel("")

    st.pyplot(fig2)

    # ---------------- TABLE ----------------
    st.subheader("📋 Records")

    st.dataframe(df, use_container_width=True)