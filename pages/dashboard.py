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

st.title("📊 Dashboard")

# ---------------- LOGIN CHECK ----------------

if "user" not in st.session_state:

    st.warning("Please login first")
    st.stop()

username = st.session_state["user"]

st.success(f"Welcome {username}")

# ---------------- QUESTIONNAIRE STATUS ----------------

if "ml_prediction" not in st.session_state:

    st.warning(
        "⚠ Please complete Questionnaire first"
    )

else:

    st.success(
        "✅ Questionnaire analysis completed"
    )

if st.session_state.get(
    "face_done",
    False
):

    st.warning(
        "Face detection already completed. Please relogin."
    )

    st.stop()
# ---------------- CAMERA ----------------

camera = st.camera_input("Take a Photo")

if camera is not None:

    file_bytes = np.asarray(
        bytearray(camera.read()),
        dtype=np.uint8
    )

    frame = cv2.imdecode(file_bytes, 1)

    face = detect_face(frame)

    if face is not None:

        # ---------------- CNN PREDICTION ----------------

        cnn_prediction = predict_stress(face)

        # ---------------- GET ML PREDICTION ----------------

        ml_prediction = st.session_state.get(
            "ml_prediction",
            1
        )

        # ---------------- HYBRID FUSION ----------------

        final_stress = hybrid_fusion(
            ml_prediction,
            cnn_prediction
        )

        # ---------------- SAVE TO DATABASE ----------------

        cursor.execute(
            """
            INSERT INTO stress_data
            (username, stress_level)
            VALUES (?, ?)
            """,
            (username, final_stress)
        )

        conn.commit()

        # ---------------- FINAL RESULT ----------------

        st.subheader("🧠 Hybrid Stress Result")

        if final_stress == "Low":

            st.success("😊 Low Stress")

        elif final_stress == "Medium":

            st.warning("😐 Medium Stress")

        else:

            st.error("😟 High Stress")

        # ---------------- SHOW MODEL SCORES ----------------

        st.write(
            f"📋 Questionnaire Score: {ml_prediction}"
        )

        st.write(
            f"📷 CNN Score: {cnn_prediction}"
        )

        st.write(
            f"🎯 Final Hybrid Result: {final_stress}"
        )

        # ---------------- AI SUGGESTIONS ----------------

        st.info(
            get_suggestion(final_stress)
        )

    else:

        st.error("No face detected")

# ---------------- LOAD HISTORY ----------------

st.subheader("📈 Stress History")

df = pd.read_sql(
    f"""
    SELECT * FROM stress_data
    WHERE username='{username}'
    """,
    conn
)

# ---------------- FILTER ----------------

option = st.selectbox(
    "Filter",
    ["All", "Today", "Last 7 Days"]
)

if not df.empty:

    df["date"] = pd.to_datetime(df["date"])

    if option == "Today":

        df = df[
            df["date"].dt.date ==
            pd.Timestamp.today().date()
        ]

    elif option == "Last 7 Days":

        df = df[
            df["date"] >
            pd.Timestamp.now() -
            pd.Timedelta(days=7)
        ]

# ---------------- CHARTS ----------------

if not df.empty:

    st.subheader("📈 Stress Trend")

    st.line_chart(df["stress_level"])

    st.subheader("📊 Stress Bar Chart")

    st.bar_chart(df["stress_level"])

    # ---------------- PIE CHART ----------------

    stress_counts = (
        df["stress_level"]
        .value_counts()
    )

    fig, ax = plt.subplots()

    ax.pie(
        stress_counts,
        labels=stress_counts.index,
        autopct='%1.1f%%'
    )

    ax.set_title(
        "Stress Distribution"
    )

    st.pyplot(fig)

    # ---------------- TABLE ----------------

    st.subheader("📋 Stress Records")

    st.dataframe(df)

else:

    st.info("No stress data available")