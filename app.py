import streamlit as st
import joblib
import re
import pandas as pd
import plotly.express as px

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Cybersecurity Dashboard", layout="centered")

# ---------------------------
# CUSTOM CSS
# ---------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #eef2f3, #dfe9f3);
}
[data-theme="dark"] .stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
}
.main-container {
    background: white;
    padding: 30px;
    border-radius: 20px;
    max-width: 900px;
    margin: auto;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.2);
}
[data-theme="dark"] .main-container {
    background: #1e1e1e;
    color: white;
}
.stButton > button {
    background: #2c5364;
    color: white;
    border-radius: 12px;
    height: 3em;
}
.card {
    padding: 15px;
    border-radius: 15px;
    margin-top: 10px;
    background: #f7f9fc;
}
[data-theme="dark"] .card {
    background: #2a2a2a;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("📚 Cybersecurity Learning Hub")

with st.sidebar.expander("🔑 Password Security"):
    st.write("Use strong passwords with symbols and numbers.")

with st.sidebar.expander("⚠️ Phishing Awareness"):
    st.write("Avoid clicking suspicious links.")

with st.sidebar.expander("🔐 MFA"):
    st.write("Enable multi-factor authentication.")

with st.sidebar.expander("🔄 Updates"):
    st.write("Always keep software updated.")

st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Trusted Resources")
st.sidebar.markdown("""
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)  
- [CISA](https://www.cisa.gov/)  
""")

# ---------------------------
# DARK MODE
# ---------------------------
theme = st.toggle("🌗 Dark Mode")
if theme:
    st.markdown('<div data-theme="dark">', unsafe_allow_html=True)

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ---------------------------
# LOAD MODEL
# ---------------------------
model = joblib.load("cyber_model.pkl")

# ---------------------------
# HEADER
# ---------------------------
st.title("🔐 Cybersecurity Risk Dashboard")

# ---------------------------
# PASSWORD STRENGTH FUNCTION
# ---------------------------
def password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Include numbers")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add special characters")

    if score <= 1:
        return "Weak", 25, "#ff4d4d", feedback, 2
    elif score <= 3:
        return "Medium", 60, "#ffa500", feedback, 1
    else:
        return "Strong", 100, "#28a745", feedback, 0

# ---------------------------
# INPUT
# ---------------------------
password_input = st.text_input("🔑 Enter Password", type="password")

# PASSWORD METER
if password_input:
    label, percent, color, feedback, score_pw = password_strength(password_input)

    st.markdown(f"""
    <div style="margin-top:10px;">
        <div style="height:10px; width:100%; background:#ddd; border-radius:5px;">
            <div style="width:{percent}%; height:10px; background:{color}; border-radius:5px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div class='card'>🔑 Password Strength: <b style='color:{color}'>{label}</b></div>", unsafe_allow_html=True)

    if feedback:
        st.markdown("<div class='card'>💡 Suggestions:</div>", unsafe_allow_html=True)
        for tip in feedback:
            st.write(f"- {tip}")
else:
    score_pw = None
    label = None

clicks = st.selectbox("Clicks suspicious links?", ["Yes","No"])
mfa = st.selectbox("Uses MFA?", ["Yes","No"])
update = st.selectbox("Update frequency", ["Rare","Occasional","Frequent"])

clicks_map = {"Yes":1,"No":0}
mfa_map = {"Yes":0,"No":1}
update_map = {"Rare":2,"Occasional":1,"Frequent":0}

# ---------------------------
# RECOMMENDATIONS
# ---------------------------
def get_recommendation(password_label, clicks, mfa, update):
    recs = []
    if password_label == "Weak": recs.append("Use stronger password")
    if mfa == "No": recs.append("Enable MFA")
    if clicks == "Yes": recs.append("Avoid suspicious links")
    if update == "Rare": recs.append("Update software regularly")
    if not recs: recs.append("Maintain good practices")
    return recs

# ---------------------------
# LEARNING RESOURCES
# ---------------------------
def get_learning_resources(risk, password_label, clicks, mfa, update):
    resources = []

    if risk == "High":
        resources += [
            ("NIST Cybersecurity Framework", "https://www.nist.gov/cyberframework"),
            ("OWASP Top 10", "https://owasp.org/www-project-top-ten/"),
            ("CISA Guide", "https://www.cisa.gov/")
        ]
    elif risk == "Medium":
        resources += [
            ("OWASP Awareness", "https://owasp.org/www-project-security-awareness/"),
            ("Google Security Tips", "https://safety.google/security/security-tips/")
        ]
    elif risk == "Low":
        resources += [
            ("NIST Password Guidelines", "https://pages.nist.gov/800-63-3/"),
            ("CISA Best Practices", "https://www.cisa.gov/")
        ]

    if password_label == "Weak":
        resources.append(("Password Guide", "https://pages.nist.gov/800-63-3/"))
    if clicks == "Yes":
        resources.append(("Phishing Prevention", "https://owasp.org/www-community/attacks/Phishing"))
    if mfa == "No":
        resources.append(("MFA Guide", "https://www.cisa.gov/mfa"))
    if update == "Rare":
        resources.append(("Update Importance", "https://staysafeonline.org/resources/"))

    return list(set(resources))

# ---------------------------
# ANALYZE
# ---------------------------
if st.button("🚀 Analyze Risk"):
    if password_input:

        values = [
            score_pw,
            clicks_map[clicks],
            mfa_map[mfa],
            update_map[update]
        ]

        df_input = pd.DataFrame([values], columns=[
            'Password_Strength',
            'Clicks_Suspicious_Links',
            'Uses_MFA',
            'Update_Frequency'
        ])

        pred = model.predict(df_input)[0]
        risk_map = {0:"Low",1:"Medium",2:"High"}
        risk = risk_map[pred]

        st.subheader(f"⚠️ Risk Level: {risk}")

        # Security Score
        score = int((1 - (sum(values)/(len(values)*2))) * 100)
        st.progress(score/100)
        st.write(f"Security Score: {score}%")

        # Recommendations
        st.subheader("🔐 Recommendations")
        for r in get_recommendation(label, clicks, mfa, update):
            st.markdown(f"<div class='card'>✔ {r}</div>", unsafe_allow_html=True)

        # ---------------------------
        # VISUAL DASHBOARD
        # ---------------------------
        st.subheader("📊 Security Behavior Analysis")

        df = pd.DataFrame({
            "Behavior": ["Password", "Links", "MFA", "Updates"],
            "Score": values
        })

        col1, col2 = st.columns(2)

        # BAR CHART
        with col1:
            fig_bar = px.bar(
                df,
                x="Behavior",
                y="Score",
                text="Score",
                color="Score",
                color_continuous_scale=["green", "orange", "red"]
            )
            fig_bar.update_layout(
                title="Behavior Risk Scores",
                yaxis_title="Risk Level (0=Low, 2=High)",
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # PIE CHART
        with col2:
            pie_df = pd.DataFrame({
                "Risk Level": ["Low", "Medium", "High"],
                "Count": [
                    values.count(0),
                    values.count(1),
                    values.count(2)
                ]
            })

            fig_pie = px.pie(
                pie_df,
                names="Risk Level",
                values="Count",
                title="Risk Distribution",
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # Resources
        st.subheader(f"🌐 Learning Resources for {risk} Risk Users")
        for name, link in get_learning_resources(risk, label, clicks, mfa, update):
            st.markdown(f"<div class='card'>🔗 <a href='{link}' target='_blank'>{name}</a></div>", unsafe_allow_html=True)

    else:
        st.warning("Enter password")

# CLOSE
st.markdown('</div>', unsafe_allow_html=True)

if theme:
    st.markdown('</div>', unsafe_allow_html=True)
