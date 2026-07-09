import os
from sqlalchemy.orm import Session
from app.database.config import SessionLocal, engine
from app.database import crud
from app.models import db_models, schemas
from app.parser.pdf_parser import extract_text_from_pdf
from app.ai_engine.gemini_client import extract_resume_info

# Create tables
db_models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

uploads_dir = "uploads"
files = [f for f in os.listdir(uploads_dir) if f.endswith('.pdf')]

for file_name in files:
    print(f"Processing {file_name}...")
    file_path = os.path.join(uploads_dir, file_name)
    text = extract_text_from_pdf(file_path)
    
    if not text.strip():
        print(f"Skipping {file_name} due to empty text.")
        continue
        
    try:
        parsed_data = extract_resume_info(text)
        if not parsed_data:
            print(f"AI Extraction failed for {file_name} (possibly rate limit). Skipping...")
            continue
            
        parsed_data["resume_text"] = text
        parsed_data["resume_file_path"] = file_path
        
        email = parsed_data.get("email")
        if email:
            existing = crud.get_candidate_by_email(db, email=email)
            if existing:
                print(f"Candidate {email} already exists. Skipping...")
                continue
                
        candidate_create = schemas.CandidateCreate(**parsed_data)
        candidate = crud.create_candidate(db=db, candidate=candidate_create)
        print(f"Successfully added candidate: {candidate.full_name} (ATS Score: {candidate.ats_score})")
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

db.close()
print("Database seeding completed.")
