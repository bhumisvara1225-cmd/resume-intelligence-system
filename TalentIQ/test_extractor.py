from app.parser.info_extractor import *

sample_text = """
BHUMISVARA M S
bhumisvara1025@gmail.com
+91 6374122965

Skills:
Python
SQL
Machine Learning
FastAPI
Git
"""

print("Name:", extract_name(sample_text))
print("Email:", extract_email(sample_text))
print("Phone:", extract_phone(sample_text))
print("Skills:", extract_skills(sample_text))