
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
from ..database.database import get_db
from ..schemas.chat_schema import ChatRequest, ChatResponse, ChatMessage
from ..schemas.diary_schema import DiaryInDB
from ..models.thought_diary_model import ThoughtDiary
from ..models.user_model import User
from ..dependencies import get_current_user
from ..services.ai_service import get_ai_response, summarize_session

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/conversation", response_model=ChatResponse)
async def chat_conversation(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """Prowadzi rozmowę z AI asystentem"""
    # Konwertuj ChatMessage na dict dla serwisu AI
    history = [{"role": msg.role, "content": msg.content} for msg in request.history]
    
    # Uzyskaj odpowiedź od AI
    ai_response_content = await get_ai_response(history)
    
    # Utwórz obiekt odpowiedzi
    response_message = ChatMessage(
        role="assistant",
        content=ai_response_content
    )
    
    return ChatResponse(message=response_message)


@router.post("/end_session", response_model=DiaryInDB, status_code=status.HTTP_201_CREATED)
async def end_chat_session(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Kończy sesję czatu i zapisuje podsumowanie w dzienniku"""
    # Konwertuj ChatMessage na dict dla serwisu AI
    history = [{"role": msg.role, "content": msg.content} for msg in request.history]
    
    try:
        # Uzyskaj podsumowanie sesji
        summary_data = await summarize_session(history)
    except (ValueError, json.JSONDecodeError, Exception) as e:
        # W przypadku błędu, utwórz podstawowe podsumowanie
        print(f"Error during session summarization: {str(e)}")
        summary_data = {
            "summary_title": "Sesja terapeutyczna",
            "session_data": {
                "situation": "Sesja została zakończona, ale automatyczne podsumowanie nie powiodło się",
                "automatic_thought": "Brak danych",
                "emotion": "Brak danych",
                "behavior": "Brak danych", 
                "cognitive_distortion": "Brak danych",
                "alternative_thought": "Brak danych",
                "action_plan": "Przejrzyj historię czatu ręcznie"
            }
        }
    
    # Utwórz nowy wpis w dzienniku
    db_diary = ThoughtDiary(
        user_id=current_user.id,
        summary_title=summary_data["summary_title"],
        session_data=summary_data["session_data"]
    )
    
    db.add(db_diary)
    db.commit()
    db.refresh(db_diary)
    
    return db_diary
