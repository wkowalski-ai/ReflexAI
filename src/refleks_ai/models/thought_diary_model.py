from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator
import json
from . import Base


class JSONType(TypeDecorator):
    """Portable JSON type that works with both SQLite and PostgreSQL."""
    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return value


class ThoughtDiary(Base):
    __tablename__ = "thought_diaries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    summary_title = Column(String, nullable=False)
    summary_description = Column(String)
    session_data = Column(JSONType, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacja z użytkownikiem
    user = relationship("User", back_populates="diaries")