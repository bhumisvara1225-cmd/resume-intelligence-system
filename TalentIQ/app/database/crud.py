from sqlalchemy.orm import Session
from app.models import db_models, schemas

def get_candidate_by_email(db: Session, email: str):
    return db.query(db_models.Candidate).filter(db_models.Candidate.email == email).first()

def get_candidate_by_id(db: Session, candidate_id: int):
    return db.query(db_models.Candidate).filter(db_models.Candidate.candidate_id == candidate_id).first()

def get_all_candidates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Candidate).offset(skip).limit(limit).all()

def create_candidate(db: Session, candidate: schemas.CandidateCreate):
    db_candidate = db_models.Candidate(
        full_name=candidate.full_name,
        email=candidate.email,
        phone=candidate.phone,
        linkedin=candidate.linkedin,
        github=candidate.github,
        portfolio=candidate.portfolio,
        address=candidate.address
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    
    for edu in candidate.education:
        db_edu = db_models.Education(**edu.model_dump(), candidate_id=db_candidate.candidate_id)
        db.add(db_edu)
        
    for exp in candidate.experience:
        db_exp = db_models.Experience(**exp.model_dump(), candidate_id=db_candidate.candidate_id)
        db.add(db_exp)
        
    for skill in candidate.skills:
        db_skill = db_models.Skill(**skill.model_dump(), candidate_id=db_candidate.candidate_id)
        db.add(db_skill)
        
    if candidate.ai_analysis:
        db_ai = db_models.AIAnalysis(
            **candidate.ai_analysis.model_dump(),
            candidate_id=db_candidate.candidate_id
        )
        db.add(db_ai)
        
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def delete_candidate(db: Session, candidate_id: int):
    candidate = get_candidate_by_id(db, candidate_id)
    if candidate:
        db.delete(candidate)
        db.commit()
    return candidate
