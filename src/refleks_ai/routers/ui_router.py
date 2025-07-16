
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.thought_diary_model import ThoughtDiary
from ..models.user_model import User
from ..dependencies import get_current_user

router = APIRouter(prefix="/ui", tags=["ui"])
templates = Jinja2Templates(directory="templates")


@router.get("/diaries", response_class=HTMLResponse)
async def get_diaries_ui(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Zwraca fragment HTML z listą dzienników użytkownika"""
    diaries = db.query(ThoughtDiary).filter(
        ThoughtDiary.user_id == current_user.id
    ).order_by(ThoughtDiary.created_at.desc()).all()
    
    return templates.TemplateResponse(
        "diary_list_partial.html", 
        {"request": request, "diaries": diaries}
    )
