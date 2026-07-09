import os
from app.database.config import SessionLocal, engine
from app.database import crud
from app.models import db_models, schemas
from app.parser.pdf_parser import extract_text_from_pdf
from app.ai_engine.gemini_client import extract_resume_info

db_models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

file_path = "uploads/Sriharan_Resume_FSD.pdf"
print(f"Processing: {file_path}")

text = extract_text_from_pdf(file_path)
if not text.strip():
    print("ERROR: Could not extract text from file!")
    db.close()
    exit()

print(f"Extracted {len(text)} characters of text.")
print("Calling Gemini API to analyze resume...")

parsed_data = extract_resume_info(text)
if not parsed_data:
    print("ERROR: Gemini API failed to analyze the resume (rate limit or API key issue).")
    db.close()
    exit()

print(f"AI Extraction Success!")
print(f"  Name: {parsed_data.get('full_name')}")
print(f"  Email: {parsed_data.get('email')}")
print(f"  ATS Score: {parsed_data.get('ai_analysis', {}).get('ats_score', 'N/A') if isinstance(parsed_data.get('ai_analysis'), dict) else 'N/A'}")

parsed_data["resume_text"] = text
parsed_data["resume_file_path"] = file_path

email = parsed_data.get("email")
if email:
    existing = crud.get_candidate_by_email(db, email=email)
    if existing:
        print(f"Candidate with email {email} already exists! Skipping.")
        db.close()
        exit()

try:
    candidate_create = schemas.CandidateCreate(**parsed_data)
    candidate = crud.create_candidate(db=db, candidate=candidate_create)
    print(f"\nSUCCESS! Added: {candidate.full_name} (ID: {candidate.candidate_id})")
except Exception as e:
    print(f"ERROR saving to database: {e}")

db.close()
