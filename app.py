import json
from pathlib import Path
from datetime import datetime

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# ──────────────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduSphere — Student Management",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATABASE = "school_data.json"

# ──────────────────────────────────────────────────────────────────────────
# DATA LAYER  (same logic as the original script, adapted for Streamlit)
# ──────────────────────────────────────────────────────────────────────────
def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE, "r") as f:
            content = f.read()
            if content:
                return json.loads(content)
    return {"students": [], "teachers": []}


def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)


if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data


def validate_email(email: str) -> bool:
    return "@" in email and "." in email


def persist():
    save_data(st.session_state.data)


# ──────────────────────────────────────────────────────────────────────────
# STYLE — the "crazy good looking" part
# ──────────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
h1, h2, h3, .stTabs [data-baseweb="tab"] p { font-family: 'Space Grotesk', sans-serif; }

/* App background */
.stApp {
    background: radial-gradient(circle at 10% 0%, #1b1035 0%, #0d0a1f 40%, #070512 100%);
    color: #eae6ff;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #150c2e 0%, #0d0a1f 100%);
    border-right: 1px solid rgba(168,133,255,0.15);
}
section[data-testid="stSidebar"] * { color: #eae6ff !important; }

/* Hero header */
.hero {
    padding: 34px 40px;
    border-radius: 22px;
    background: linear-gradient(120deg, #7c3aed 0%, #db2777 55%, #f97316 100%);
    box-shadow: 0 20px 60px -20px rgba(124,58,237,0.6);
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: "";
    position: absolute; inset: 0;
    background: radial-gradient(circle at 85% 20%, rgba(255,255,255,0.25), transparent 45%);
}
.hero h1 {
    color: white; font-size: 2.4rem; margin: 0; font-weight: 700;
    letter-spacing: -0.5px;
}
.hero p { color: rgba(255,255,255,0.9); margin-top: 6px; font-size: 1.02rem; }

/* Glass cards */
.glass-card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(168,133,255,0.18);
    border-radius: 18px;
    padding: 22px 24px;
    backdrop-filter: blur(6px);
    transition: all 0.25s ease;
}
.glass-card:hover {
    border-color: rgba(168,133,255,0.5);
    transform: translateY(-3px);
    box-shadow: 0 12px 34px -10px rgba(124,58,237,0.45);
}

/* Metric tiles */
.metric-tile {
    border-radius: 18px;
    padding: 20px 22px;
    background: linear-gradient(135deg, rgba(124,58,237,0.25), rgba(219,39,119,0.12));
    border: 1px solid rgba(168,133,255,0.25);
}
.metric-label { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.2px; color: #c9b8ff; }
.metric-value { font-size: 2.1rem; font-weight: 700; color: white; font-family: 'Space Grotesk', sans-serif; }
.metric-sub { font-size: 0.78rem; color: #9d8fc9; }

/* Student/teacher result card */
.person-card {
    border-radius: 16px;
    padding: 18px 22px;
    background: rgba(255,255,255,0.04);
    border-left: 4px solid #db2777;
    margin-bottom: 12px;
}
.person-card .name { font-size: 1.15rem; font-weight: 700; color: white; }
.person-card .meta { color: #b7a9e0; font-size: 0.88rem; }
.badge {
    display: inline-block; padding: 2px 10px; border-radius: 999px;
    font-size: 0.72rem; font-weight: 600; margin-right: 6px;
    background: rgba(124,58,237,0.25); color: #d8c8ff; border: 1px solid rgba(168,133,255,0.35);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(120deg, #7c3aed, #db2777);
    color: white; border: none; border-radius: 12px;
    padding: 10px 18px; font-weight: 600; letter-spacing: 0.2px;
    transition: all 0.2s ease;
    box-shadow: 0 8px 22px -8px rgba(124,58,237,0.7);
}
.stButton>button:hover { transform: translateY(-2px); box-shadow: 0 12px 28px -8px rgba(219,39,119,0.6); }

/* Danger button (delete) */
.danger-zone .stButton>button {
    background: linear-gradient(120deg, #dc2626, #991b1b);
    box-shadow: 0 8px 22px -8px rgba(220,38,38,0.7);
}
.danger-zone .stButton>button:hover { box-shadow: 0 12px 28px -8px rgba(220,38,38,0.6); }

/* Inputs */
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
    background: rgba(255,255,255,0.06) !important;
    color: #eae6ff !important;
    border-radius: 10px !important;
    border: 1px solid rgba(168,133,255,0.25) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 6px; }
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.04);
    border-radius: 10px 10px 0 0;
    padding: 8px 18px;
    color: #b7a9e0;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(120deg, #7c3aed, #db2777) !important;
    color: white !important;
}

hr { border-color: rgba(168,133,255,0.15); }

/* Hide default streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────
# HERO
# ──────────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="hero">
    <h1>🎓 EduSphere</h1>
    <p>A slicker way to manage students, teachers & grades — powered by your JSON database.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────
# SIDEBAR NAV
# ──────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🧭 Navigate")
    page = st.radio(
        "Go to",
        [
            "📊 Dashboard",
            "📝 Register Student",
            "🧑‍🏫 Register Teacher",
            "✏️ Add Grades",
            "🔍 Student Lookup",
            "🔍 Teacher Lookup",
            "📚 All Students",
            "🗂️ All Teachers",
            "🗑️ Delete Student",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption(f"💾 Database: `{DATABASE}`")
    st.caption(f"🕒 {datetime.now().strftime('%b %d, %Y — %I:%M %p')}")

n_students = len(data["students"])
n_teachers = len(data["teachers"])
all_avgs = [
    sum(s["grades"].values()) / len(s["grades"])
    for s in data["students"]
    if s["grades"]
]
overall_avg = round(sum(all_avgs) / len(all_avgs), 2) if all_avgs else 0

# ──────────────────────────────────────────────────────────────────────────
# DASHBOARD
# ──────────────────────────────────────────────────────────────────────────
if page == "📊 Dashboard":
    c1, c2, c3, c4 = st.columns(4)
    tiles = [
        ("Total Students", n_students, "👩‍🎓"),
        ("Total Teachers", n_teachers, "🧑‍🏫"),
        ("Overall Avg Grade", f"{overall_avg}", "📈"),
        ("Subjects Taught", len({t["subject"] for t in data["teachers"]}), "📘"),
    ]
    for col, (label, val, icon) in zip([c1, c2, c3, c4], tiles):
        with col:
            st.markdown(
                f"""<div class="metric-tile">
                        <div class="metric-label">{icon} {label}</div>
                        <div class="metric-value">{val}</div>
                    </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    colA, colB = st.columns([1.3, 1])

    with colA:
        st.markdown("#### 📈 Average Grade per Student")
        if data["students"]:
            names, avgs = [], []
            for s in data["students"]:
                if s["grades"]:
                    names.append(s["name"])
                    avgs.append(round(sum(s["grades"].values()) / len(s["grades"]), 2))
            if names:
                fig = go.Figure(
                    go.Bar(
                        x=names,
                        y=avgs,
                        marker=dict(
                            color=avgs,
                            colorscale=[[0, "#7c3aed"], [1, "#f97316"]],
                            line=dict(width=0),
                        ),
                        text=avgs,
                        textposition="outside",
                    )
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#eae6ff",
                    margin=dict(t=10, l=10, r=10, b=10),
                    yaxis=dict(gridcolor="rgba(168,133,255,0.12)"),
                    height=340,
                )
                st.plotly_chart(fig, width="stretch")
            else:
                st.info("No grades recorded yet.")
        else:
            st.info("No students registered yet.")

    with colB:
        st.markdown("#### 📘 Teachers by Subject")
        if data["teachers"]:
            subj_counts = {}
            for t in data["teachers"]:
                subj_counts[t["subject"]] = subj_counts.get(t["subject"], 0) + 1
            fig2 = px.pie(
                names=list(subj_counts.keys()),
                values=list(subj_counts.values()),
                hole=0.55,
                color_discrete_sequence=["#7c3aed", "#db2777", "#f97316", "#22d3ee", "#a855f7"],
            )
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#eae6ff",
                margin=dict(t=10, l=10, r=10, b=10),
                height=340,
                showlegend=True,
                legend=dict(orientation="h", y=-0.1),
            )
            st.plotly_chart(fig2, width="stretch")
        else:
            st.info("No teachers registered yet.")

# ──────────────────────────────────────────────────────────────────────────
# REGISTER STUDENT
# ──────────────────────────────────────────────────────────────────────────
elif page == "📝 Register Student":
    st.markdown("### 📝 Register a New Student")
    with st.form("register_student", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=1, max_value=120, step=1)
        with c2:
            email = st.text_input("Email")
            roll_no = st.number_input("Roll Number", min_value=0, step=1)
        submitted = st.form_submit_button("✨ Register Student")

    if submitted:
        if not name.strip():
            st.error("Name cannot be empty.")
        elif not validate_email(email):
            st.error("❌ Invalid email address.")
        elif any(s["roll_no"] == roll_no for s in data["students"]):
            st.error(f"⚠️ A student with roll number {roll_no} already exists.")
        else:
            data["students"].append(
                {
                    "name": name.strip(),
                    "age": int(age),
                    "email": email.strip(),
                    "roll_no": int(roll_no),
                    "grades": {},
                }
            )
            persist()
            st.success(f"✅ Student **{name}** registered successfully!")
            st.balloons()

# ──────────────────────────────────────────────────────────────────────────
# REGISTER TEACHER
# ──────────────────────────────────────────────────────────────────────────
elif page == "🧑‍🏫 Register Teacher":
    st.markdown("### 🧑‍🏫 Register a New Teacher")
    with st.form("register_teacher", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=18, max_value=100, step=1)
            subject = st.text_input("Subject")
        with c2:
            email = st.text_input("Email")
            emp_id = st.number_input("Employee ID", min_value=0, step=1)
        submitted = st.form_submit_button("✨ Register Teacher")

    if submitted:
        if not name.strip():
            st.error("Name cannot be empty.")
        elif not validate_email(email):
            st.error("❌ Invalid email address.")
        elif not subject.strip():
            st.error("Subject cannot be empty.")
        elif any(t["emp_id"] == emp_id for t in data["teachers"]):
            st.error(f"⚠️ A teacher with employee ID {emp_id} already exists.")
        else:
            data["teachers"].append(
                {
                    "name": name.strip(),
                    "age": int(age),
                    "email": email.strip(),
                    "emp_id": int(emp_id),
                    "subject": subject.strip(),
                }
            )
            persist()
            st.success(f"✅ Teacher **{name}** registered successfully!")
            st.balloons()

# ──────────────────────────────────────────────────────────────────────────
# ADD GRADES
# ──────────────────────────────────────────────────────────────────────────
elif page == "✏️ Add Grades":
    st.markdown("### ✏️ Add / Update a Grade")
    if not data["students"]:
        st.info("No students registered yet — register one first.")
    else:
        options = {f'{s["name"]} (Roll #{s["roll_no"]})': s["roll_no"] for s in data["students"]}
        with st.form("add_grades"):
            chosen = st.selectbox("Select Student", list(options.keys()))
            subject = st.text_input("Subject")
            marks = st.number_input("Marks", min_value=0.0, max_value=100.0, step=0.5)
            submitted = st.form_submit_button("💾 Save Grade")

        if submitted:
            roll_no = options[chosen]
            if not subject.strip():
                st.error("Subject cannot be empty.")
            else:
                for s in data["students"]:
                    if s["roll_no"] == roll_no:
                        s["grades"][subject.strip()] = marks
                        persist()
                        st.success(f"✅ Grade for **{subject}** ({marks}) saved for {s['name']}.")
                        break

# ──────────────────────────────────────────────────────────────────────────
# STUDENT LOOKUP
# ──────────────────────────────────────────────────────────────────────────
elif page == "🔍 Student Lookup":
    st.markdown("### 🔍 Look Up a Student")
    if not data["students"]:
        st.info("No students registered yet.")
    else:
        roll_no = st.number_input("Enter Roll Number", min_value=0, step=1)
        if st.button("Search"):
            found = next((s for s in data["students"] if s["roll_no"] == roll_no), None)
            if found:
                grades = found["grades"]
                avg = round(sum(grades.values()) / len(grades), 2) if grades else 0
                st.markdown(
                    f"""<div class="person-card">
                        <div class="name">👩‍🎓 {found['name']}</div>
                        <div class="meta">Roll No: {found['roll_no']} &nbsp;•&nbsp; Age: {found['age']} &nbsp;•&nbsp; {found['email']}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.metric("Average Grade", avg)
                    if grades:
                        for subj, mark in grades.items():
                            st.markdown(f"<span class='badge'>{subj}: {mark}</span>", unsafe_allow_html=True)
                    else:
                        st.caption("No grades recorded yet.")
                with c2:
                    if grades:
                        fig = px.bar(
                            x=list(grades.keys()),
                            y=list(grades.values()),
                            color=list(grades.values()),
                            color_continuous_scale=["#7c3aed", "#f97316"],
                        )
                        fig.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            font_color="#eae6ff",
                            height=260,
                            margin=dict(t=10, l=10, r=10, b=10),
                            coloraxis_showscale=False,
                        )
                        st.plotly_chart(fig, width="stretch")
            else:
                st.error("🚫 Student not found.")

# ──────────────────────────────────────────────────────────────────────────
# TEACHER LOOKUP
# ──────────────────────────────────────────────────────────────────────────
elif page == "🔍 Teacher Lookup":
    st.markdown("### 🔍 Look Up a Teacher")
    if not data["teachers"]:
        st.info("No teachers registered yet.")
    else:
        emp_id = st.number_input("Enter Employee ID", min_value=0, step=1)
        if st.button("Search"):
            found = next((t for t in data["teachers"] if t["emp_id"] == emp_id), None)
            if found:
                st.markdown(
                    f"""<div class="person-card">
                        <div class="name">🧑‍🏫 {found['name']}</div>
                        <div class="meta">Employee ID: {found['emp_id']} &nbsp;•&nbsp; Age: {found['age']} &nbsp;•&nbsp; {found['email']}</div>
                        <span class="badge">📘 {found['subject']}</span>
                    </div>""",
                    unsafe_allow_html=True,
                )
            else:
                st.error("🚫 Teacher not found.")

# ──────────────────────────────────────────────────────────────────────────
# ALL STUDENTS
# ──────────────────────────────────────────────────────────────────────────
elif page == "📚 All Students":
    st.markdown("### 📚 All Students")
    if not data["students"]:
        st.info("No students registered yet.")
    else:
        search = st.text_input("🔎 Filter by name")
        rows = data["students"]
        if search:
            rows = [s for s in rows if search.lower() in s["name"].lower()]
        for s in rows:
            grades = s["grades"]
            avg = round(sum(grades.values()) / len(grades), 2) if grades else "—"
            grade_str = ", ".join(f"{k}: {v}" for k, v in grades.items()) or "No grades yet"
            card_col, btn_col = st.columns([6, 1])
            with card_col:
                st.markdown(
                    f"""<div class="person-card">
                        <div class="name">👩‍🎓 {s['name']} <span class="badge">Roll #{s['roll_no']}</span></div>
                        <div class="meta">Age {s['age']} • {s['email']}</div>
                        <div class="meta">🎯 Avg: <b>{avg}</b> &nbsp;|&nbsp; {grade_str}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            with btn_col:
                st.markdown('<div class="danger-zone">', unsafe_allow_html=True)
                if st.button("🗑️", key=f"quick_del_{s['roll_no']}", help="Delete this student"):
                    data["students"] = [x for x in data["students"] if x["roll_no"] != s["roll_no"]]
                    persist()
                    st.success(f"🗑️ {s['name']} deleted.")
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# ALL TEACHERS
# ──────────────────────────────────────────────────────────────────────────
elif page == "🗂️ All Teachers":
    st.markdown("### 🗂️ All Teachers")
    if not data["teachers"]:
        st.info("No teachers registered yet.")
    else:
        search = st.text_input("🔎 Filter by name")
        rows = data["teachers"]
        if search:
            rows = [t for t in rows if search.lower() in t["name"].lower()]
        for t in rows:
            st.markdown(
                f"""<div class="person-card">
                    <div class="name">🧑‍🏫 {t['name']} <span class="badge">ID #{t['emp_id']}</span></div>
                    <div class="meta">Age {t['age']} • {t['email']}</div>
                    <div class="meta">📘 Subject: <b>{t['subject']}</b></div>
                </div>""",
                unsafe_allow_html=True,
            )

# ──────────────────────────────────────────────────────────────────────────
# DELETE STUDENT
# ──────────────────────────────────────────────────────────────────────────
elif page == "🗑️ Delete Student":
    st.markdown("### 🗑️ Delete a Student")
    if not data["students"]:
        st.info("No students registered yet.")
    else:
        options = {f'{s["name"]} (Roll #{s["roll_no"]})': s["roll_no"] for s in data["students"]}
        chosen = st.selectbox("Select Student to Delete", list(options.keys()))
        roll_no = options[chosen]
        found = next((s for s in data["students"] if s["roll_no"] == roll_no), None)

        if found:
            grades = found["grades"]
            avg = round(sum(grades.values()) / len(grades), 2) if grades else "—"
            st.markdown(
                f"""<div class="person-card">
                    <div class="name">👩‍🎓 {found['name']} <span class="badge">Roll #{found['roll_no']}</span></div>
                    <div class="meta">Age {found['age']} • {found['email']}</div>
                    <div class="meta">🎯 Avg: <b>{avg}</b></div>
                </div>""",
                unsafe_allow_html=True,
            )

            confirm = st.checkbox(f"⚠️ I confirm I want to permanently delete **{found['name']}**")
            st.markdown('<div class="danger-zone">', unsafe_allow_html=True)
            if st.button("🗑️ Delete Student", disabled=not confirm):
                data["students"] = [x for x in data["students"] if x["roll_no"] != roll_no]
                persist()
                st.success(f"✅ {found['name']} was deleted successfully.")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)