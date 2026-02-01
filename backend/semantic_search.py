from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

DOMAIN_QUERIES = {
    "Machine Learning": "machine learning deep learning ml neural networks computer vision nlp",
    "Data Science": "data science analytics statistics python pandas numpy sql visualization",
    "Web Development": "web development django flask react javascript frontend backend",
    "Cloud / DevOps": "cloud computing aws azure gcp docker kubernetes devops",
    "Android Development": "android development kotlin java android studio"
}


def build_search_text(sections):
    summary = []

    if sections.get("skills"):
        summary.append(
            "The candidate has skills in " +
            sections["skills"].replace("\n", " ")
        )

    if sections.get("projects"):
        summary.append(
            "The candidate has worked on projects such as " +
            sections["projects"].replace("\n", " ")
        )

    if sections.get("experience"):
        summary.append(
            "The candidate has professional experience including " +
            sections["experience"].replace("\n", " ")
        )

    if sections.get("achievements"):
        summary.append(
            "The candidate achieved " +
            sections["achievements"].replace("\n", " ")
        )

    return ". ".join(summary)

class ResumeSemanticSearch:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.resume_ids = []
        self.embeddings = []

    def index_resumes(self, resume_data):
        """
        resume_data = [
          {
            "resume": "resume_1.txt",
            "sections": {...}
          }
        ]
        """
        texts = []
        for r in resume_data:
            # Prefer pre-flattened text if provided
            if "text" in r:
                text = r["text"]
            else:
                text = build_search_text(r["sections"])

            texts.append(text)
            self.resume_ids.append(r.get("Resume") or r.get("resume"))

        self.embeddings = self.model.encode(texts, convert_to_numpy=True)

    def search(self, query, top_k=5):
        query_vec = self.model.encode([query], convert_to_numpy=True)
        scores = cosine_similarity(query_vec, self.embeddings)[0]

        ranked = sorted(
            zip(self.resume_ids, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_k]

    def classify_by_domain(self, domain_queries, threshold=0.20):
        """
        Returns:
        {
        "Machine Learning": ["resume_1.txt", "resume_3.txt"],
        "Data Science": ["resume_18.txt"]
        }
        """

        domain_groups = {d: [] for d in domain_queries}

        for domain, query in domain_queries.items():
            results = self.search(query, top_k=len(self.resume_ids))

            for resume_id, score in results:
                if score >= threshold:
                    domain_groups[domain].append(resume_id)

        return domain_groups
