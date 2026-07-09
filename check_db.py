from app.database.config import SessionLocal
from app.models.db_models import Candidate, AIAnalysis

db = SessionLocal()
candidates = db.query(Candidate).all()

print(f"Total candidates in DB: {len(candidates)}")
print("-" * 60)
for c in candidates:
    ats = c.ai_analysis.ats_score if c.ai_analysis else "NO AI ANALYSIS"
    print(f"ID: {c.candidate_id} | Name: {c.full_name} | Email: {c.email} | ATS: {ats}")

db.close()
