import os
from docx import Document
import pdfplumber

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_docx(file_path)
    elif file_path.endswith(".txt"):
        return extract_txt(file_path)
    else:
        return ""

def extract_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
def extract_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)
