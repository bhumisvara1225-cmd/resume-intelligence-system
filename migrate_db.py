import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "resume_intelligence.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
try:
    cursor.execute("ALTER TABLE ai_analysis ADD COLUMN ats_score INTEGER;")
    conn.commit()
    print("Successfully added ats_score column")
except sqlite3.OperationalError as e:
    print(f"Column might already exist or other error: {e}")
finally:
    conn.close()
