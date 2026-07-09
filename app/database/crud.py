from sqlalchemy.orm import Session
from app.models import db_models, schemas

def get_candidate_by_email(db: Session, email: str):
    return db.query(db_models.Candidate).filter(db_models.Candidate.email == email).first()

def get_candidate(db: Session, candidate_id: int):
    return db.query(db_models.Candidate).filter(db_models.Candidate.candidate_id == candidate_id).first()

def create_candidate(db: Session, candidate: schemas.CandidateCreate):
    db_candidate = db_models.Candidate(
        full_name=candidate.full_name,
        email=candidate.email,
        phone=candidate.phone,
        linkedin=candidate.linkedin,
        github=candidate.github,
        portfolio=candidate.portfolio,
        address=candidate.address,
        resume_text=candidate.resume_text,
        resume_file_path=candidate.resume_file_path
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

def get_candidates(
    db: Session, 
    search_query: str = None, 
    skill_filter: str = None, 
    role_filter: str = None,
    limit: int = 100,
    skip: int = 0
):
    query = db.query(db_models.Candidate)
    
    if search_query:
        search = f"%{search_query}%"
        query = query.filter(
            (db_models.Candidate.full_name.ilike(search)) | 
            (db_models.Candidate.email.ilike(search))
        )
        
    if skill_filter:
        query = query.join(db_models.Candidate.skills).filter(
            db_models.Skill.skill_name.ilike(f"%{skill_filter}%")
        )
        
    if role_filter:
        query = query.join(db_models.Candidate.experience).filter(
            db_models.Experience.role.ilike(f"%{role_filter}%")
        )
        
    return query.offset(skip).limit(limit).all()
