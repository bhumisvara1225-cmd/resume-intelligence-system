from app.database.db import engine
from app.models.resume_model import Base
from app.models.candidate_model import Candidate

Base.metadata.create_all(bind=engine)

print("Tables created successfully")