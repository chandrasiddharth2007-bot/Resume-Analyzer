SECTION_HEADERS = {
    "education": ["education", "academic"],
    "skills": ["skills", "technical skills"],
    "experience": ["experience", "internship"],
    "projects": ["projects"],
    "achievements": ["achievements", "awards"],
    "extras": ["activities", "languages", "hobbies"]
}

def split_sections(text):
    sections = {k: "" for k in SECTION_HEADERS}
    current = None

    for line in text.split("\n"):
        l = line.lower()
        for section, keys in SECTION_HEADERS.items():
            if any(k in l for k in keys):
                current = section
                break
        if current:
            sections[current] += line + "\n"

    return sections
