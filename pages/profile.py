import streamlit as st
import pandas as pd

from database.db import conn

st.title("👤 User Profile")

# ---------------- LOGIN CHECK ----------------

if "user" not in st.session_state:

    st.warning("Please login first")

    st.stop()

username = st.session_state["user"]

st.success(f"Logged in as: {username}")

# ---------------- LOAD USER DATA ----------------

df = pd.read_sql(
    f"""
    SELECT * FROM stress_data
    WHERE username='{username}'
    """,
    conn
)

# ---------------- PROFILE INFO ----------------

st.subheader("📋 User Information")

st.write(f"👤 Username: {username}")

st.write(f"📊 Total Records: {len(df)}")

# ---------------- STRESS HISTORY ----------------

if not df.empty:

    st.subheader("📈 Stress History")

    # ---------------- DELETE BUTTON ----------------

    col1, col2 = st.columns([20, 1])

    with col2:

        st.write("")

        with st.popover("🗑"):

            st.warning(
                "Confirm delete history?"
            )

            if st.button(
                "Delete History",
                use_container_width=True
            ):

                cursor = conn.cursor()

                cursor.execute(
                    """
                    DELETE FROM stress_data
                    WHERE username=?
                    """,
                    (username,)
                )

                conn.commit()

                st.success(
                    "History deleted successfully"
                )

                st.rerun()

    # ---------------- TABLE ----------------

    st.dataframe(
        df,
        use_container_width=True
    )

    # ---------------- AVERAGE STRESS ----------------

    stress_map = {
        "Low": 0,
        "Medium": 1,
        "High": 2,
        0: 0,
        1: 1,
        2: 2
    }

    df["stress_numeric"] = (
        df["stress_level"]
        .map(stress_map)
    )

    avg_stress = (
        df["stress_numeric"]
        .mean()
    )

    st.metric(
        "Average Stress Score",
        round(avg_stress, 2)
    )

    # ---------------- OVERALL STATUS ----------------

    if avg_stress < 0.8:

        st.success(
            "😊 Overall Low Stress"
        )

    elif avg_stress < 1.5:

        st.warning(
            "😐 Overall Medium Stress"
        )

    else:

        st.error(
            "😟 Overall High Stress"
        )

    # ---------------- DOWNLOAD REPORT ----------------

    csv = df.to_csv(index=False)

    st.download_button(
        "⬇ Download Stress Report",
        csv,
        file_name="stress_report.csv",
        mime="text/csv"
    )

else:

    st.info("No stress history found")