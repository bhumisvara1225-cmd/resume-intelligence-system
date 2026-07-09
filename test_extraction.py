import os
from dotenv import load_dotenv
import google.generativeai as genai
from app.ai_engine.gemini_client import extract_resume_info

load_dotenv()
resume_text = """
John Doe
Software Engineer
Skills: Python, React, SQL
Experience: 3 years at Tech Corp
Education: B.S. in Computer Science
"""
result = extract_resume_info(resume_text)
print(result)
