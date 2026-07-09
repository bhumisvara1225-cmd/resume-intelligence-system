import re


def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group() if match else None


def extract_phone(text):
    match = re.search(r'(\+91[- ]?)?[6-9]\d{9}', text)
    return match.group() if match else None


def extract_linkedin(text):
    match = re.search(r'linkedin\.com/in/\S+', text, re.IGNORECASE)
    return match.group() if match else None


def extract_github(text):
    match = re.search(r'github\.com/\S+', text, re.IGNORECASE)
    return match.group() if match else None


def extract_name(text):
    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if len(line) > 3 and len(line.split()) <= 4:
            return line

    return None
SKILLS = [
    "python",
    "java",
    "sql",
    "mysql",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pandas",
    "numpy",
    "fastapi",
    "flask",
    "git",
    "github",
    "data analysis"
]


def extract_skills(text):
    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text_lower:
            found_skills.append(skill)

    return list(set(found_skills))