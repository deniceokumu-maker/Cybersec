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

/* Background */
.stApp {
    background: linear-gradient(to right, #eef2f3, #dfe9f3);
}

/* Dark mode */
[data-theme="dark"] .stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
}

/* Main container */
.main-container {
    background: white;
    padding: 30px;
    border-radius: 20px;
    max-width: 900px;
    margin: auto;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.2);
    animation: fadeIn 1s ease-in;
}

/* Dark container */
[data-theme="dark"] .main-container {
    background: #1e1e1e;
    color: white;
}

/* Buttons */
.stButton > button {
    background: #2c5364;
    color: white;
    border-radius: 12px;
    height: 3em;
    font-size: 16px;
    transition: 0.3s;
}
.stButton > button:hover {
    background: #1b3c4a;
    transform: scale(1.05);
}

/* Cards */
.card {
    padding: 15px;
    border-radius: 15px;
    margin-top: 10px;
    background: #f7f9fc;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
}
[data-theme="dark"] .card {
    background: #2a2a2a;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #2c5364, #203a43);
    color: white;
}

/* Animation */
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR LEARNING HUB
# ---------------------------
st.sidebar.title("📚 Cybersecurity Learning Hub")

with st.sidebar.expander("🔑 Password Security"):
    st.markdown("""
- Use strong passwords (8+ characters)
- Include uppercase, numbers, symbols
- Avoid common passwords
""")

with st.sidebar.expander("⚠️ Phishing Awareness"):
    st.markdown("""
- Avoid suspicious links
- Verify email senders
- Watch for urgency scams
""")

with st.sidebar.expander("🔐 MFA"):
    st.markdown("""
- Adds extra security layer
- Protects even if password is stolen
""")

with st.sidebar.expander("🔄 Updates"):
    st.markdown("""
- Fix vulnerabilities
- Always enable auto-updates
""")

st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Trusted Resources")

st.sidebar.markdown("""
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)  
- [CISA Cybersecurity](https://www.cisa.gov/)  
- [Stay Safe Online](https://staysafeonline.org/)  
""")

# ---------------------------
# DARK MODE
# ---------------------------
theme = st.toggle("🌗 Dark Mode")

if theme:
    st.markdown('<div data-theme="dark">', unsafe_allow_html=True)

# ---------------------------
# MAIN CONTAINER
# ---------------------------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ---------------------------
# LOAD MODEL
# ---------------------------
model = joblib.load("cyber_model.pkl")

# ---------------------------
# HEADER
# ---------------------------
st.title("🔐 Cybersecurity Risk Dashboard")
st.markdown("### Analyze your behavior and improve your security posture")
st.markdown("---")

# ---------------------------
# PASSWORD FUNCTION
# ---------------------------
def password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    if score <= 1:
        return "Weak", 2
    elif score <= 3:
        return "Medium", 1
    else:
        return "Strong", 0

# ---------------------------
# INPUT SECTION
# ---------------------------
st.subheader("🧾 Enter Your Security Details")

col1, col2 = st.columns(2)

with col1:
    password_input = st.text_input("🔑 Password")
    clicks = st.selectbox("⚠️ Click Suspicious Links?", ["Yes", "No"])

with col2:
    mfa = st.selectbox("🔐 Uses MFA?", ["Yes", "No"])
    update = st.selectbox("🔄 Update Frequency", ["Rare", "Occasional", "Frequent"])

clicks_map = {"Yes": 1, "No": 0}
mfa_map = {"Yes": 0, "No": 1}
update_map = {"Rare": 2, "Occasional": 1, "Frequent": 0}

# ---------------------------
# RECOMMENDATIONS
# ---------------------------
def get_recommendation(password_label, clicks, mfa, update):
    recs = []
    if password_label == "Weak":
        recs.append("Use a strong password")
    if mfa == "No":
        recs.append("Enable MFA")
    if clicks == "Yes":
        recs.append("Avoid suspicious links")
    if update == "Rare":
        recs.append("Update software regularly")
    if not recs:
        recs.append("Maintain good practices")
    return recs

# ---------------------------
# LEARNING RESOURCES
# ---------------------------
def get_learning_resources(risk, password_label, clicks, mfa, update):
    resources = []

    if risk == "High":
        resources.append(("NIST Cybersecurity Framework", "https://www.nist.gov/cyberframework"))
        resources.append(("OWASP Top 10", "https://owasp.org/www-project-top-ten/"))

    if password_label == "Weak":
        resources.append(("NIST Password Guidelines", "https://pages.nist.gov/800-63-3/"))

    if clicks == "Yes":
        resources.append(("Phishing Prevention", "https://owasp.org/www-community/attacks/Phishing"))

    if mfa == "No":
        resources.append(("CISA MFA Guide", "https://www.cisa.gov/mfa"))

    if update == "Rare":
        resources.append(("Stay Safe Online", "https://staysafeonline.org/resources/"))

    return list(set(resources))

# ---------------------------
# ANALYZE
# ---------------------------
st.markdown("---")

if st.button("🚀 Analyze Risk"):
    if password_input:

        password_label, password_score = password_strength(password_input)

        values = [
            password_score,
            clicks_map[clicks],
            mfa_map[mfa],
            update_map[update]
        ]

        input_data = pd.DataFrame([values], columns=[
            'Password_Strength',
            'Clicks_Suspicious_Links',
            'Uses_MFA',
            'Update_Frequency'
        ])

        prediction = model.predict(input_data)[0]
        risk_map = {0: "Low", 1: "Medium", 2: "High"}
        risk = risk_map[prediction]

        # RESULTS
        st.subheader("📊 Results")

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        if risk == "High":
            st.error("⚠️ High Risk")
        elif risk == "Medium":
            st.warning("⚠️ Medium Risk")
        else:
            st.success("✅ Low Risk")

        st.write(f"🔑 Password Strength: {password_label}")
        st.markdown("</div>", unsafe_allow_html=True)

        # SECURITY SCORE
        score = int((1 - (sum(values) / (len(values) * 2))) * 100)

        st.subheader("📊 Security Score")
        st.progress(score / 100)
        st.write(f"Score: {score}%")

        # RECOMMENDATIONS
        st.subheader("🔐 Recommendations")
        for rec in get_recommendation(password_label, clicks, mfa, update):
            st.markdown(f"<div class='card'>✔ {rec}</div>", unsafe_allow_html=True)

        # VISUALS
        df = pd.DataFrame({
            "Behavior": ["Password", "Links", "MFA", "Updates"],
            "Risk Score": values
        })

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(px.bar(df, x="Behavior", y="Risk Score", text="Risk Score"))

        with col2:
            pie_df = pd.DataFrame({
                "Level": ["Low", "Medium", "High"],
                "Count": [values.count(0), values.count(1), values.count(2)]
            })
            st.plotly_chart(px.pie(pie_df, names="Level", values="Count"))

        # DYNAMIC RESOURCES
        st.subheader("🌐 Recommended Learning Resources")

        for name, link in get_learning_resources(risk, password_label, clicks, mfa, update):
            st.markdown(f"<div class='card'>🔗 <a href='{link}' target='_blank'>{name}</a></div>", unsafe_allow_html=True)

    else:
        st.warning("Enter password")

# CLOSE
st.markdown('</div>', unsafe_allow_html=True)

if theme:
    st.markdown('</div>', unsafe_allow_html=True)
