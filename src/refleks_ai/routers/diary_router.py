
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..schemas.diary_schema import DiaryCreate, DiaryUpdate, DiaryInDB
from ..models.thought_diary_model import ThoughtDiary
from ..models.user_model import User
from ..dependencies import get_current_user

router = APIRouter(prefix="/diaries", tags=["diaries"])


@router.get("/", response_model=List[DiaryInDB])
async def get_diaries(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Zwraca listę dzienników dla zalogowanego użytkownika"""
    diaries = db.query(ThoughtDiary).filter(
        ThoughtDiary.user_id == current_user.id
    ).all()
    return diaries


@router.get("/{diary_id}", response_model=DiaryInDB)
async def get_diary(
    diary_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Zwraca jeden dziennik na podstawie jego ID"""
    diary = db.query(ThoughtDiary).filter(
        ThoughtDiary.id == diary_id,
        ThoughtDiary.user_id == current_user.id
    ).first()
    
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diary not found"
        )
    
    return diary


@router.post("/", response_model=DiaryInDB, status_code=status.HTTP_201_CREATED)
async def create_diary(
    diary_data: DiaryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Tworzy nowy wpis w dzienniku"""
    db_diary = ThoughtDiary(
        user_id=current_user.id,
        summary_title=diary_data.summary_title,
        session_data=diary_data.session_data
    )
    
    db.add(db_diary)
    db.commit()
    db.refresh(db_diary)
    
    return db_diary


@router.patch("/{diary_id}", response_model=DiaryInDB)
async def update_diary(
    diary_id: int,
    diary_update: DiaryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Aktualizuje pole summary_title wpisu"""
    diary = db.query(ThoughtDiary).filter(
        ThoughtDiary.id == diary_id,
        ThoughtDiary.user_id == current_user.id
    ).first()
    
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diary not found"
        )
    
    if diary_update.summary_title is not None:
        diary.summary_title = diary_update.summary_title
    
    db.commit()
    db.refresh(diary)
    
    return diary


@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(
    diary_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Usuwa wpis z dziennika"""
    diary = db.query(ThoughtDiary).filter(
        ThoughtDiary.id == diary_id,
        ThoughtDiary.user_id == current_user.id
    ).first()
    
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diary not found"
        )
    
    db.delete(diary)
    db.commit()
