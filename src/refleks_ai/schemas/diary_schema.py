
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, Optional


class DiaryBase(BaseModel):
    summary_title: Optional[str] = None


class DiaryCreate(DiaryBase):
    session_data: Dict[str, Any]


class DiaryUpdate(DiaryBase):
    pass


class DiaryInDB(DiaryBase):
    id: int
    user_id: int
    created_at: datetime
    session_data: Dict[str, Any]

    class Config:
        from_attributes = True
