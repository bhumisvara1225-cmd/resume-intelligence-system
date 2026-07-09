from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class EducationBase(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None
    cgpa: Optional[str] = None

class ExperienceBase(BaseModel):
    company_name: Optional[str] = None
    role: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None

class SkillBase(BaseModel):
    skill_name: Optional[str] = None
    skill_type: Optional[str] = None

class AIAnalysisBase(BaseModel):
    candidate_summary: Optional[str] = None
    recommended_roles: Optional[str] = None
    suitability_scores: Optional[str] = None
    strengths: Optional[str] = None
    ats_score: Optional[int] = None

class CandidateBase(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    address: Optional[str] = None
    resume_text: Optional[str] = None
    resume_file_path: Optional[str] = None

class CandidateCreate(CandidateBase):
    education: List[EducationBase] = []
    experience: List[ExperienceBase] = []
    skills: List[SkillBase] = []
    ai_analysis: Optional[AIAnalysisBase] = None

class CandidateResponse(CandidateBase):
    candidate_id: int
    education: List[EducationBase] = []
    experience: List[ExperienceBase] = []
    skills: List[SkillBase] = []
    ai_analysis: Optional[AIAnalysisBase] = None

    model_config = ConfigDict(from_attributes=True)
