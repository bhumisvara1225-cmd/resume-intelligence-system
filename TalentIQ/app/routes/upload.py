from app.models.candidate_model import Candidate
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import os
import shutil

from app.database.db import get_db
from app.models.resume_model import Resume

from app.parser.pdf_parser import extract_text_from_pdf
from app.parser.docx_parser import extract_text_from_docx

from app.parser.info_extractor import (
    extract_name,
    extract_email,
    extract_phone,
    extract_skills
)

router = APIRouter()


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    os.makedirs("uploads", exist_ok=True)

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = ""

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(filepath)

    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(filepath)

    # Extract candidate information
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)

    # Save raw resume
    resume = Resume(
        filename=file.filename,
        content=text
    )

    db.add(resume)
    db.commit()

    return {
        "message": "Resume processed successfully",
        "filename": file.filename,
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills
    }


@router.get("/resumes")
def get_resumes(db: Session = Depends(get_db)):
    resumes = db.query(Resume).all()

    return [
        {
            "id": r.id,
            "filename": r.filename
        }
        for r in resumes
    ]