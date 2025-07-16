
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user_model import User
from .thought_diary_model import ThoughtDiary

__all__ = ["Base", "User", "ThoughtDiary"]
