import uuid

from sqlalchemy import Column, Index, Text, Integer, CheckConstraint, String
from sqlalchemy.dialects.postgresql import UUID

from .engine import BaseORM


class LearningText(BaseORM):
    __tablename__ = "learning_texts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False, unique=True)
    difficulty = Column(Integer, nullable=True, unique=False)
    value = Column(Text, nullable=False, unique=False)
    transcription = Column(Text, nullable=False, unique=False)

    __table_args__ = (
        Index("learning_text_title_idx", title, postgresql_using="hash"),
        CheckConstraint(difficulty >= 0, name="check_difficulty_is_positive"),
    )
