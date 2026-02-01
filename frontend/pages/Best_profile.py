import streamlit as st
import os
import sys
import json
import pandas as pd

# ------------------ Path Setup ------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.semantic_search import ResumeSemanticSearch

OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

st.set_page_config(page_title="Best Profile Fit", layout="wide")

# ------------------ Guard States ------------------
if st.session_state.get("analysis_running", False):
    st.info("⏳ Analysis is running. Please wait for it to complete.")
    st.stop()

ranking_path = os.path.join(OUTPUT_DIR, "ranking.csv")
extracted_path = os.path.join(OUTPUT_DIR, "extracted.json")

if not os.path.exists(ranking_path) or not os.path.exists(extracted_path):
    st.warning("Please analyze resumes on the main page first.")
    st.stop()

# ------------------ Load Data ------------------
ranking_df = pd.read_csv(ranking_path)

with open(extracted_path) as f:
    extracted_data = json.load(f)

# ------------------ UI ------------------
st.markdown("""
<h1 class="gradient-text">🎯 Best Profile Fit</h1>
<p style="color:#94a3b8;">
Find the best candidates for a role using semantic AI matching.
</p>
""", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)

job_query = st.text_area(
    "Describe the role",
    placeholder="e.g. Machine learning intern with Python, NLP, and projects"
)

top_k = st.slider("Number of candidates", 1, 10, 5)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------ Matching ------------------
if st.button("🔍 Find Best Fit"):

    search_engine = ResumeSemanticSearch()

    results = []
    for resume, sections in extracted_data.items():
        score = ranking_df.loc[
            ranking_df["Resume"] == resume, "Score"
        ].values[0]

        results.append({
            "resume": resume,
            "score": score,
            "sections": sections
        })

    search_engine.index_resumes(results)

    matches = search_engine.search(job_query, top_k=top_k)

    st.subheader("🏆 Best Matching Candidates")

    for resume, similarity in matches:
        base_score = ranking_df.loc[
            ranking_df["Resume"] == resume, "Score"
        ].values[0]

        fit_score = round((similarity * 100 + base_score) / 2, 2)

        st.markdown(
            f"""
            <div class="domain-card">
                <div class="domain-title">📄 {resume}</div>
                <div class="domain-item">Semantic Match: {round(similarity, 2)}</div>
                <div class="domain-item">Resume Score: {base_score}</div>
                <div class="domain-item"><b>Overall Fit: {fit_score}</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )
