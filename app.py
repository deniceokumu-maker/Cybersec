
import streamlit as st
import joblib
import matplotlib.pyplot as plt
import re

# Load model
model = joblib.load("cyber_model.pkl")

st.set_page_config(page_title="Cybersecurity Risk System", layout="wide")

st.title("🔐 Cybersecurity Risk & Recommendation System")
st.write("Analyze your cybersecurity behavior and get personalized recommendations.")

# ---------------------------
# PASSWORD STRENGTH FUNCTION
# ---------------------------
def password_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1

    if score <= 1:
        return "Weak", 2
    elif score <= 3:
        return "Medium", 1
    else:
        return "Strong", 0

# ---------------------------
# USER INPUTS
# ---------------------------
st.subheader("Enter Your Security Details")

password_input = st.text_input("Enter Your Password")

clicks = st.select_slider("Clicks Suspicious Links?", ["Yes", "No"])
mfa = st.select_slider("Uses Multi-Factor Authentication (MFA)?", ["Yes", "No"])
update = st.select_slider("Software Update Frequency", ["Rare", "Occasional", "Frequent"])

# Encoding maps
clicks_map = {"Yes": 1, "No": 0}
mfa_map = {"Yes": 0, "No": 1}
update_map = {"Rare": 2, "Occasional": 1, "Frequent": 0}

# ---------------------------
# RECOMMENDATION LOGIC
# ---------------------------
def get_recommendation(password_label, clicks, mfa, update):
    recs = []

    if password_label == "Weak":
        recs.append("Use a strong password with uppercase, numbers, and symbols")
    if mfa == "No":
        recs.append("Enable Multi-Factor Authentication (MFA)")
    if clicks == "Yes":
        recs.append("Avoid clicking suspicious links")
    if update == "Rare":
        recs.append("Update your software regularly")

    if not recs:
        recs.append("Maintain good cybersecurity practices")

    return recs

# ---------------------------
# ANALYZE BUTTON
# ---------------------------
if st.button("Analyze Risk"):
    if password_input:

        # Detect password strength
        password_label, password_score = password_strength(password_input)

        st.subheader(f"🔑 Password Strength: {password_label}")

        # Prepare input for model
        input_data = [
            password_score,
            clicks_map[clicks],
            mfa_map[mfa],
            update_map[update]
        ]

        prediction = model.predict([input_data])[0]

        risk_map = {0: "Low", 1: "Medium", 2: "High"}
        risk = risk_map[prediction]

        st.subheader(f"⚠️ Predicted Risk Level: {risk}")

        # Recommendations
        recommendations = get_recommendation(password_label, clicks, mfa, update)

        st.subheader("🔐 Recommendations:")
        for rec in recommendations:
            st.success(rec)

        # ---------------------------
        # VISUALS
        # ---------------------------
        behaviors = ["Password", "Suspicious Links", "MFA", "Updates"]
        values = [
            password_score,
            clicks_map[clicks],
            mfa_map[mfa],
            update_map[update]
        ]

        colors = ["red" if v==2 else "orange" if v==1 else "green" for v in values]

        # Bar Chart
        fig, ax = plt.subplots()
        ax.bar(behaviors, values, color=colors)
        ax.set_ylabel("Risk Score (0=Good, 2=High Risk)")
        ax.set_ylim(0,2.5)
        ax.set_title("User Behavior Risk Scores")
        st.pyplot(fig)

        # Pie Chart
        risk_counts = [values.count(0), values.count(1), values.count(2)]
        fig2, ax2 = plt.subplots()
        ax2.pie(risk_counts, labels=["Low","Medium","High"], autopct='%1.1f%%')
        ax2.set_title("Risk Distribution")
        st.pyplot(fig2)

    else:
        st.warning("Please enter a password to analyze.")
