import re

def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def safe_float(val):
    try:
        return float(val)
    except:
        return None

