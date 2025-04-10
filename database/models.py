import uuid

from sqlalchemy import Column, Index, Text, CheckConstraint, String
from sqlalchemy.dialects.postgresql import UUID, SMALLINT

from .engine import BaseORM


class LearningText(BaseORM):
    """ORM таблицы, содержащей информацию по обучающим текстам."""

    __tablename__ = "learning_texts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False, unique=True)
    difficulty = Column(SMALLINT, nullable=False, default=0, unique=False)
    preview = Column(String(500), nullable=True, unique=False)
    value = Column(Text, nullable=False, unique=False)
    transcription = Column(Text, nullable=False, unique=False)

    __table_args__ = (
        Index("learning_text_title_idx", title, postgresql_using="hash"),
        CheckConstraint(difficulty >= 0, name="check_text_difficulty_is_positive"),
    )
