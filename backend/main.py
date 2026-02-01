from extractor import extract_text
from section_splitter import split_sections
from scorer import score_resume
from utils import normalize_text
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESUME_DIR = os.path.join(BASE_DIR, "resumes")

results = []

for file in os.listdir(RESUME_DIR):
    path = os.path.join(RESUME_DIR, file)

    if not os.path.isfile(path):
        continue

    text = extract_text(path)
    sections = split_sections(text)
    score = score_resume(sections)

    results.append({
        "resume": file,
        "score": score,
        "sections": sections
    })



# Ranking
ranked = sorted(results, key=lambda x: x["score"], reverse=True)

print("\nFINAL RANKING\n")
for idx, r in enumerate(ranked, start=1):
    print(f"{idx}. {r['resume']} → {r['score']}")

file = "resume_1.txt"
path = os.path.join(RESUME_DIR, file)
print("\n")
text = extract_text(path)
sections = split_sections(text)
score = score_resume(sections)
for a,b in sections.items():
        sections[a] = sections[a].replace("\n", " ").strip()
def pretty_print_sections(sections):
    print("\n--- EXTRACTED RESUME DATA ---\n")
    for section, content in sections.items():
        if content.strip():
            print(f"[{section.upper()}]")
            print(content.strip())
            print("-" * 40)
pretty_print_sections(sections)

from semantic_search import ResumeSemanticSearch, DOMAIN_QUERIES

search_engine = ResumeSemanticSearch()
search_engine.index_resumes(results)

domain_groups = search_engine.classify_by_domain(
    DOMAIN_QUERIES,
    threshold=0.22
)


print("\n📂 RESUME CLASSIFICATION BY DOMAIN (SEMANTIC)\n")

for domain, resumes in domain_groups.items():
    if resumes:
        print(domain)
        for r in resumes:
            print(r)
        print()
