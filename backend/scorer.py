import re

WEIGHTS = {
    "internships": 20,
    "skills": 20,
    "projects": 15,
    "cgpa": 10,
    "achievements": 10
}

def extract_cgpa(text):
    match = re.search(r'cgpa[:\s]*([\d\.]{3,4})', text.lower())
    if match:
        try:
            return float(match.group(1))
        except:
            return None
    return None


def score_skills(text):
    skills = re.split(r',|\n|\|', text)
    skills = [s.strip() for s in skills if len(s.strip()) > 2]
    count = len(set(skills))
    if count >= 10: return 20
    if count >= 7: return 16
    if count >= 4: return 12
    if count >= 1: return 6
    return 0

def score_projects(text):
    count = len([l for l in text.split("\n") if len(l.strip()) > 20])
    return min(count * 3, 15)

def score_internships(text):
    count = text.lower().count("intern")
    return min(count * 10, 20)

def score_achievements(text):
    count = text.count("%") + text.count("rank")
    return min(count * 5, 10)

def score_resume(sections):
    score = 0

    score += score_skills(sections["skills"])
    score += score_projects(sections["projects"])
    score += score_internships(sections["experience"])
    score += score_achievements(sections["achievements"])

    cgpa = extract_cgpa(sections["education"])
    if cgpa:
        score += min((cgpa / 10) * 10, 10)

    return round(score, 2)
def score_resume(sections, return_breakdown=False):
    breakdown = {
        "Internships": 20 if "intern" in sections["experience"].lower() else 0,
        "Skills": min(len(sections["skills"].split(",")) * 2, 20),
        "Projects": min(sections["projects"].count("\n") * 5, 15),
        "CGPA": 10 if "cgpa" in sections["education"].lower() else 0,
        "Achievements": 10 if sections["achievements"] else 0,
        "Experience": 5 if sections["experience"] else 0,
        "Extras": 5 if sections["extras"] else 0
    }

    total = sum(breakdown.values())

    if return_breakdown:
        return total, breakdown

    return total
