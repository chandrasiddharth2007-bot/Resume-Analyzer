import streamlit as st
import os
import sys
import plotly.express as px

# ------------------ Path Setup ------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.extractor import extract_text
from backend.section_splitter import split_sections
from backend.scorer import score_resume
from backend.semantic_search import ResumeSemanticSearch, DOMAIN_QUERIES

st.set_page_config(page_title="Single Resume Analysis", layout="wide")

# ------------------ UI Header ------------------
st.markdown("""
<h1 class="gradient-text">📊 Single Resume Analysis</h1>
<p style="color:#94a3b8;">
Upload one resume to view detailed analysis and visual insights.
</p>
""", unsafe_allow_html=True)

# ------------------ Upload ------------------
uploaded_file = st.file_uploader(
    "Upload ONE resume (PDF / DOCX / TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=False
)

if not uploaded_file:
    st.info("Please upload a resume to begin analysis.")
    st.stop()

# ------------------ Process Resume ------------------
with st.spinner("Analyzing resume..."):
    temp_path = os.path.join(BASE_DIR, "resumes", uploaded_file.name)
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    text = extract_text(temp_path)
    sections = split_sections(text)
    total_score, score_breakdown = score_resume(sections, return_breakdown=True)

# ------------------ Semantic Domain Analysis ------------------
search_engine = ResumeSemanticSearch()

resume_payload = [{
    "resume": uploaded_file.name,
    "score": total_score,
    "sections": sections
}]

search_engine.index_resumes(resume_payload)

domain_scores = {}

for domain, query in DOMAIN_QUERIES.items():
    matches = search_engine.search(query, top_k=1)

    if matches and matches[0][0] == uploaded_file.name:
        domain_scores[domain] = matches[0][1]
    else:
        domain_scores[domain] = 0.0


# ------------------ Layout ------------------
col1, col2 = st.columns(2)

# ------------------ Pie Chart: Score Breakdown ------------------
with col1:
    st.subheader("📊 Resume Score Breakdown")

    pie1 = px.pie(
        names=list(score_breakdown.keys()),
        values=list(score_breakdown.values()),
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    pie1.update_layout(showlegend=True)
    st.plotly_chart(pie1, use_container_width=True)

# ------------------ Pie Chart: Domain Confidence ------------------
with col2:
    st.subheader("🧠 Domain Confidence Distribution")

    pie2 = px.pie(
        names=list(domain_scores.keys()),
        values=list(domain_scores.values()),
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    pie2.update_layout(showlegend=True)
    st.plotly_chart(pie2, use_container_width=True)

# ------------------ Summary Card ------------------
st.markdown(f"""
<div class="card">
<h3>⭐ Overall Resume Score: {round(total_score, 2)} / 100</h3>
<p style="color:#94a3b8;">
Primary Domain: <b>{max(domain_scores, key=domain_scores.get)}</b>
</p>
</div>
""", unsafe_allow_html=True)

# ------------------ Extracted Sections ------------------
st.subheader("📄 Extracted Resume Sections")

for section, content in sections.items():
    if content.strip():
        st.markdown(f"""
        <div class="card">
        <h4>{section.title()}</h4>
        <p style="white-space: pre-wrap;">{content}</p>
        </div>
        """, unsafe_allow_html=True)
