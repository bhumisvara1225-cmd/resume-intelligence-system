from sqlalchemy import Column, Integer, String, Text
from app.models.resume_model import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))

    skills = Column(Text)