import streamlit as st
import os
from groq import Groq
from datetime import date, time

# ---------------- CONFIG ----------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="Multi-Agent AI System",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "email_sent" not in st.session_state:
    st.session_state.email_sent = False

# ---------------- STYLING ----------------
st.markdown(
    """
    <style>
    body {
        background-color: #0b1220;
        color: #e5e7eb;
    }

    .hero {
        padding: 90px 20px 70px;
        text-align: center;
        background: radial-gradient(circle at top, #1e3a8a, #0b1220 60%);
    }

    .hero h1 {
        font-size: 3.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #34d399, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        font-size: 1.2rem;
        color: #dbeafe;
        margin-top: 16px;
        line-height: 1.6;
    }

    .card {
        background: #111827;
        border-radius: 18px;
        padding: 36px;
        height: 100%;
        border: 1px solid #1f2933;
        transition: all 0.3s ease;
    }

    .card:hover {
        transform: translateY(-6px);
        border-color: #60a5fa;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }

    .card h3 {
        margin-bottom: 10px;
        font-size: 1.35rem;
        color: #ffffff;
    }

    .card p {
        color: #9ca3af;
        font-size: 1rem;
        line-height: 1.55;
    }

    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin: 24px 0 16px;
        color: #f9fafb;
    }

    .cta button {
        background: linear-gradient(90deg, #3b82f6, #22c55e);
        color: white;
        padding: 14px 40px;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 999px;
        border: none;
        box-shadow: 0 10px 30px rgba(59,130,246,0.4);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- HOME ----------------
def home():
    st.markdown(
        """
        <div class="hero">
            <h1>Multi-Agent AI System</h1>
            <p>
                Plan tasks, schedule meetings, draft emails,<br>
                and manage your daily operations effortlessly.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card">
                <h3>🧠 Planning</h3>
                <p>Create structured plans and break down goals into clear, manageable steps.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <h3>⚙️ Execution</h3>
                <p>Schedule meetings, draft emails, and handle operational tasks efficiently.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="card">
                <h3>🔁 Automation</h3>
                <p>Reduce manual effort by streamlining repeated workflows and routines.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    col_mid = st.columns([1, 1, 1])
    with col_mid[1]:
        st.markdown('<div class="cta">', unsafe_allow_html=True)
        if st.button("🚀 Get Started"):
            st.session_state.page = "app"
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- APP ----------------
def app():
    st.markdown("<div class='section-title'>🛠 Operations Console</div>", unsafe_allow_html=True)

    task_type = st.selectbox(
        "What would you like to do?",
        [
            "🧠 Plan tasks",
            "📘 Create a learning roadmap",
            "📅 Schedule a meeting",
            "✉️ Draft an email",
            "🗂 Organize work"
        ]
    )

    # -------- MEETING --------
    if task_type == "📅 Schedule a meeting":
        st.markdown("<div class='section-title'>📅 Schedule a Meeting</div>", unsafe_allow_html=True)

        title = st.text_input("Meeting title")
        m_date = st.date_input("Meeting date", min_value=date.today())
        m_time = st.time_input("Meeting time", value=time(10, 0))
        duration = st.selectbox("Duration", ["15 mins", "30 mins", "45 mins", "60 mins"])

        if st.button("Confirm Schedule"):
            st.success("Meeting scheduled successfully")
            st.info("Calendar entry created (simulation mode).")
        return

    # -------- EMAIL --------
    if task_type == "✉️ Draft an email":
        st.markdown("<div class='section-title'>✉️ Draft Email</div>", unsafe_allow_html=True)

        recipient = st.text_input("Recipient email")
        subject = st.text_input("Subject")
        context = st.text_area("Email details")

        if st.button("Generate Draft"):
            st.session_state.email_sent = False
            with st.spinner("Preparing email..."):
                draft = client.chat.completions.create(
                    messages=[{
                        "role": "user",
                        "content": f"Write a professional email.\nTo:{recipient}\nSubject:{subject}\nContext:{context}"
                    }],
                    model="llama-3.1-8b-instant",
                )
            st.success("Draft ready")
            st.write(draft.choices[0].message.content)

        if st.button("Send Email"):
            st.session_state.email_sent = True

        if st.session_state.email_sent:
            st.success("Email sent successfully (simulation).")
        return

    # -------- PLANNING / OTHER --------
    request = st.text_area("Describe your requirement")

    if st.button("Generate Output"):
        with st.spinner("Processing..."):
            result = client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": f"Task:{task_type}\nRequirement:{request}"
                }],
                model="llama-3.1-8b-instant",
            )
        st.success("Output generated")
        st.write(result.choices[0].message.content)

# ---------------- ROUTING ----------------
if st.session_state.page == "home":
    home()
else:
    app()