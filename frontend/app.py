import streamlit as st
import os
import sys
import json
import pandas as pd

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="AI Resume Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------ Path Setup ------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.extractor import extract_text
from backend.section_splitter import split_sections
from backend.scorer import score_resume
from backend.semantic_search import ResumeSemanticSearch, DOMAIN_QUERIES

RESUME_DIR = os.path.join(BASE_DIR, "resumes")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(RESUME_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

DOMAIN_COLORS = {
    "Machine Learning": "#6366f1",
    "Data Science": "#22d3ee",
    "Web Development": "#22c55e",
    "Cloud / DevOps": "#f97316",
    "Android Development": "#ef4444"
}

# ------------------ Session State ------------------
if "analysis_running" not in st.session_state:
    st.session_state.analysis_running = False

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

# ------------------ Header ------------------
st.markdown("""
<h1 class="gradient-text">🤖 AI Resume Intelligence</h1>
<p style="color:#94a3b8;">
Automated resume extraction, scoring, ranking & semantic domain intelligence.
</p>
""", unsafe_allow_html=True)

st.caption("Automated Extraction • Scoring • Ranking • Semantic Analysis")

# ------------------ Upload Card ------------------
st.markdown("""
<div class="card">
<h3>📤 Upload Resumes</h3>
<p style="color:#94a3b8;">
Drag & drop multiple resumes. Supported formats: PDF, DOCX, TXT.
</p>
</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

analyze = st.button("🚀 Analyze Resumes")

# ------------------ Analysis Logic ------------------
if analyze and not st.session_state.analysis_running:

    if not uploaded_files:
        st.warning("Please upload at least one resume.")
        st.stop()

    st.session_state.analysis_running = True
    st.session_state.analysis_done = False

    progress = st.progress(0)
    status = st.empty()

    results = []
    extracted_data = {}
    total = len(uploaded_files)

    for idx, file in enumerate(uploaded_files, start=1):
        status.write(f"🔍 Processing {file.name}")
        progress.progress(int((idx / total) * 100))

        path = os.path.join(RESUME_DIR, file.name)
        with open(path, "wb") as f:
            f.write(file.getbuffer())

        text = extract_text(path)
        sections = split_sections(text)
        score = score_resume(sections)

        results.append({
            "resume": file.name,
            "score": score,
            "sections": sections
        })

        extracted_data[file.name] = sections

    # ------------------ Save Outputs ------------------
    ranking_df = pd.DataFrame(
        [{"Resume": r["resume"], "Score": r["score"]} for r in results]
    ).sort_values(by="Score", ascending=False)

    ranking_df.to_csv(os.path.join(OUTPUT_DIR, "ranking.csv"), index=False)

    with open(os.path.join(OUTPUT_DIR, "extracted.json"), "w") as f:
        json.dump(extracted_data, f, indent=2)

    search_engine = ResumeSemanticSearch()
    search_engine.index_resumes(results)

    domain_groups = search_engine.classify_by_domain(
        DOMAIN_QUERIES,
        threshold=0.22
    )

    with open(os.path.join(OUTPUT_DIR, "domains.json"), "w") as f:
        json.dump(domain_groups, f, indent=2)

    st.session_state.analysis_running = False
    st.session_state.analysis_done = True

    status.success("✅ Resume analysis completed")

# ------------------ Output Section ------------------
if st.session_state.analysis_done:

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🏆 Ranked Resumes")
    ranking_df = pd.read_csv(os.path.join(OUTPUT_DIR, "ranking.csv"))
    st.dataframe(ranking_df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("🧠 Domain Classification")

    with open(os.path.join(OUTPUT_DIR, "domains.json")) as f:
        domain_groups = json.load(f)

    st.markdown("<div class='domain-grid'>", unsafe_allow_html=True)

    for domain, resumes in domain_groups.items():
        if not resumes:
            continue

        accent = DOMAIN_COLORS.get(domain, "#a78bfa")

        st.markdown(
            f"""
            <div class="domain-card" style="border-top:4px solid {accent};">
                <div class="domain-title">{domain}</div>
                {''.join(f"<div class='domain-item'>• {r}</div>" for r in resumes)}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.info(f"📄 {len(ranking_df)} resumes successfully analyzed")

# ------------------ Styling ------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #1e293b 0%, #020617 40%, #020617 100%);
    color: #e5e7eb;
}
h1, h2, h3 {
    color: #f8fafc;
    font-weight: 700;
}
.card {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(14px);
    padding: 1.4rem;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 20px 40px rgba(0,0,0,0.45);
    margin-bottom: 1.4rem;
}
.stButton > button {
    background: linear-gradient(90deg, #6366f1, #22d3ee);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
}
.domain-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.8rem;
    margin-top: 1.8rem;
}
@media (min-width: 1200px) {
    .domain-grid {
        grid-template-columns: repeat(4, 1fr);
    }
}
.domain-card {
    background: #020617;
    border-radius: 20px;
    padding: 1.4rem;
    min-height: 180px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 25px 50px rgba(0,0,0,0.6);
    transition: all 0.3s ease;
}
.domain-card:hover {
    transform: translateY(-8px) scale(1.02);
}
.domain-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 0.6rem;
}
.domain-item {
    color: #c7d2fe;
    font-size: 0.9rem;
}
.gradient-text {
    background: linear-gradient(90deg, #22d3ee, #a78bfa, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)
