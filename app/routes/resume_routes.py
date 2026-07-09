from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import shutil
from typing import List

from app.database.config import get_db
from app.database import crud
from app.models import schemas
from app.parser.pdf_parser import extract_text_from_pdf
from app.parser.docx_parser import extract_text_from_docx
from app.ai_engine.gemini_client import extract_resume_info

router = APIRouter(prefix="/api/resumes", tags=["Resumes"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=schemas.CandidateResponse)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
        
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Extract text
    if file.filename.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_docx(file_path)
        
    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from the file")
        
    # Analyze with Gemini
    parsed_data = extract_resume_info(text)
    if not parsed_data:
        raise HTTPException(status_code=500, detail="Failed to analyze resume with AI. Please check your Gemini API key.")
        
    parsed_data["resume_text"] = text
    parsed_data["resume_file_path"] = file_path
        
    email = parsed_data.get("email")
    if email:
        existing = crud.get_candidate_by_email(db, email=email)
        if existing:
            raise HTTPException(status_code=409, detail=f"Duplicate candidate: A resume with email '{email}' already exists.")
            
    try:
        candidate_create = schemas.CandidateCreate(**parsed_data)
        candidate = crud.create_candidate(db=db, candidate=candidate_create)
        return candidate
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/upload_bulk")
async def upload_bulk_resumes(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    results = []
    for file in files:
        try:
            res = await upload_resume(file, db)
            results.append({"filename": file.filename, "status": "success", "data": res})
        except Exception as e:
            # Check if e is HTTPException
            if isinstance(e, HTTPException):
                message = e.detail
            else:
                message = str(e)
            results.append({"filename": file.filename, "status": "error", "message": message})
            
    return results

@router.get("/", response_model=List[schemas.CandidateResponse])
async def get_candidates_endpoint(
    search: str = None,
    skill: str = None,
    role: str = None,
    limit: int = 100,
    skip: int = 0,
    db: Session = Depends(get_db)
):
    candidates = crud.get_candidates(
        db=db,
        search_query=search,
        skill_filter=skill,
        role_filter=role,
        limit=limit,
        skip=skip
    )
    return candidates

@router.get("/{candidate_id}/score")
async def get_role_score(candidate_id: int, role: str, db: Session = Depends(get_db)):
    candidate = crud.get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
        
    if not candidate.resume_text:
        return {"ats_score": 0, "matching_keywords": []}
        
    from app.ai_engine.gemini_client import calculate_role_score
    result = calculate_role_score(candidate.resume_text, role)
    return result
