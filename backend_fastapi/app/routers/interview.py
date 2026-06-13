import os
import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import httpx
from ..config import API_KEY
from ..database import get_db, User
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api", tags=["Interview"])

SYSTEM_PROMPT = "Ты — строгий IT-интервьюер. Задавай глубокие технические вопросы по выбранному направлению и грейду. Всего 5 вопросов. Оценивай строго, реагируй на воду и неуверенность"

class InterviewRequest(BaseModel):
    direction: str
    grade: str
    email: str

class InterviewResponse(BaseModel):
    questions: list[str]
    answers: list[str] | None = None

async def call_gemini(prompt: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ]
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        # Extract generated text
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            raise HTTPException(status_code=502, detail="Unexpected Gemini response")

@router.post("/interview", response_model=InterviewResponse)
async def generate_interview(req: InterviewRequest, db: Session = Depends(get_db)):
    # Retrieve or create user
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        user = User(email=req.email)
        db.add(user)
        db.commit()
        db.refresh(user)
    if not user.is_premium and user.free_interviews <= 0:
        raise HTTPException(status_code=403, detail="No remaining free interviews. Upgrade to premium.")
    # Decrement free interviews if not premium
    if not user.is_premium:
        user.free_interviews -= 1
        db.commit()
    # Build Gemini prompt
    prompt = f"{SYSTEM_PROMPT}\n\nСгенерируй 5 вопросов по теме '{req.direction}' для уровня '{req.grade}'."
    result_text = await call_gemini(prompt)
    # Split into questions (simple split by line numbers or newlines)
    questions = [q.strip() for q in result_text.split('\n') if q.strip()]
    return InterviewResponse(questions=questions)
