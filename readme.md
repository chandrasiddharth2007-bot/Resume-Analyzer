<h1>🤖 AI Resume Intelligence System</h1>
<p class="badge">Automated Resume Analysis • Scoring • Ranking • Semantic Intelligence</p>
<div class="card">
<h2>📌 Overview</h2>
<p>
Modern recruitment systems receive resumes in large volumes and highly inconsistent formats
(PDF, DOCX, TXT). Manual screening is slow, subjective, and non-scalable.
</p>
<p>
This project implements an <b>Automated Resume Intelligence System</b> that converts unstructured
resumes into structured data, applies a consistent scoring mechanism, performs semantic
domain analysis, and ranks candidates objectively.
</p>
</div>
<div class="card">
<h2>🎯 Key Features</h2>
<ul>
<li>Unstructured resume parsing (PDF, DOCX, TXT)</li>
<li>Rule-based, explainable resume scoring (max score: 100)</li>
<li>Objective ranking of 25+ resumes</li>
<li>Semantic domain classification using embeddings</li>
<li>Multi-domain candidate profiling</li>
<li>Single-resume analytics with visual charts</li>
<li>Best profile fit based on job description</li>
</ul>
</div>
<div class="card">
<h2>📊 Resume Scoring Weights</h2>
<table>
<tr><th>Feature</th><th>Weight</th></tr>
<tr><td>Prior Internships</td><td>20%</td></tr>
<tr><td>Skills & Certifications</td><td>20%</td></tr>
<tr><td>Projects</td><td>15%</td></tr>
<tr><td>CGPA</td><td>10%</td></tr>
<tr><td>Achievements</td><td>10%</td></tr>
<tr><td>Experience</td><td>5%</td></tr>
<tr><td>Extra-curricular</td><td>5%</td></tr>
<tr><td>Language Fluency</td><td>3%</td></tr>
<tr><td>Online Presence</td><td>3%</td></tr>
<tr><td>Degree Type</td><td>3%</td></tr>
<tr><td>College Ranking</td><td>2%</td></tr>
<tr><td>School Marks</td><td>2%</td></tr>
</table>
</div>
<div class="card">
<h2>🧠 Semantic Domain Intelligence</h2>
<p>
The system uses sentence embeddings to classify resumes into multiple domains such as
Machine Learning, Data Science, Web Development, and Software Engineering.
</p>
      <p>
        Candidates are modeled as <b>multi-domain profiles</b> with confidence scores rather than
        forced single-label classification.
      </p>
    </div>

<div class="card">
      <h2>🖥️ Tech Stack</h2>
      <ul>
        <li>Python 3.9+</li>
        <li>Streamlit (Frontend)</li>
        <li>Sentence Transformers (MiniLM)</li>
        <li>PyTorch</li>
        <li>Plotly (Charts)</li>
        <li>Rule-based NLP logic</li>
      </ul>
    </div>

<div class="card">
      <h2>🚀 How to Run</h2>
      <pre>
python -m venv myenv
myenv\Scripts\activate
pip install streamlit sentence-transformers torch plotly python-docx pdfplumber pandas
python -m streamlit run frontend/app.py
      </pre>
    </div>

<div class="card">
      <h2>🧠 Design Philosophy</h2>
      <ul>
        <li>Explainability over black-box models</li>
        <li>Fair and consistent scoring</li>
        <li>Robust to missing or noisy data</li>
        <li>Scalable and reproducible</li>
      </ul>
    </div>

<div class="card">
      <h2>🔮 Future Enhancements</h2>
      <ul>
        <li>Domain confidence bars</li>
        <li>Resume comparison dashboard</li>
        <li>Bias-awareness indicators</li>
        <li>PDF resume analytics report</li>
        <li>Dynamic job-aware scoring</li>
      </ul>
    </div>
<footer>
      <p><b>Author:</b> Siddharth Chandra</p>
      <p>AI Resume Intelligence System • 2026</p>
</footer>

</div>