from fastapi import FastAPI
from app.routes.upload import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "TalentIQ Resume Intelligence Engine Running"}