from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.config import Base

class Candidate(Base):
    __tablename__ = "candidates"
    
    candidate_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255))
    email = Column(String(255), index=True)
    phone = Column(String(50))
    linkedin = Column(Text)
    github = Column(Text)
    portfolio = Column(Text)
    address = Column(Text)
    
    education = relationship("Education", back_populates="candidate", cascade="all, delete-orphan")
    experience = relationship("Experience", back_populates="candidate", cascade="all, delete-orphan")
    skills = relationship("Skill", back_populates="candidate", cascade="all, delete-orphan")
    ai_analysis = relationship("AIAnalysis", back_populates="candidate", cascade="all, delete-orphan", uselist=False)


class Education(Base):
    __tablename__ = "education"
    
    education_id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id"))
    degree = Column(String(255))
    institution = Column(String(255))
    year = Column(String(50))
    cgpa = Column(String(50))
    
    candidate = relationship("Candidate", back_populates="education")


class Experience(Base):
    __tablename__ = "experience"
    
    experience_id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id"))
    company_name = Column(String(255))
    role = Column(String(255))
    duration = Column(String(100))
    description = Column(Text)
    
    candidate = relationship("Candidate", back_populates="experience")


class Skill(Base):
    __tablename__ = "skills"
    
    skill_id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id"))
    skill_name = Column(String(255))
    skill_type = Column(String(100))  # e.g., 'Technical', 'Soft', 'Language'
    
    candidate = relationship("Candidate", back_populates="skills")


class AIAnalysis(Base):
    __tablename__ = "ai_analysis"
    
    analysis_id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id"), unique=True)
    candidate_summary = Column(Text)
    recommended_roles = Column(Text)
    suitability_scores = Column(Text)
    strengths = Column(Text)
    
    candidate = relationship("Candidate", back_populates="ai_analysis")
