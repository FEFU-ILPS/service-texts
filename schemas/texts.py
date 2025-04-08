from pydantic import BaseModel, Field
from typing import Annotated, Optional
from uuid import UUID


class LearningTextResponse(BaseModel):
    """Данные, отправляемые в ответ на запрос получения всех текстов."""

    id: Annotated[UUID, Field(..., description="Уникальный идентификатор")]
    title: Annotated[str, Field(max_length=100, description="Название")]
    difficulty: Annotated[Optional[int], Field(ge=0, le=10, description="Сложность", default=0)]
    preview: Annotated[Optional[str], Field(max_length=500, description="Краткое описание")]


class DetailLearningTextResponse(LearningTextResponse):
    """Данные, отправляемые в ответ на запрос получения деталей о тексте."""

    value: Annotated[str, Field(..., description="Содержание")]
    transcription: Annotated[str, Field(..., description="Транскрипционная запись")]


class CreateLearningTextRequest(BaseModel):
    """Данные, требующиеся для создания/добавления текста в систему."""

    title: Annotated[str, Field(max_length=100, description="Название")]
    difficulty: Annotated[Optional[int], Field(ge=0, le=10, description="Сложность", default=0)]
    preview: Annotated[Optional[str], Field(max_length=500, description="Краткое описание")]
    value: Annotated[str, Field(..., description="Содержание")]
    # TODO: Разработать алгоритм, позволяющий создать default factory преобразования текста в транскрипцию
    # ! Позже можно сделать Optional
    transcription: Annotated[str, Field(..., description="Транскрипционная запись")]


class CreateLearningTextResponse(BaseModel):
    """Данные, отправляемые в ответ на запрос добавления текста."""

    id: Annotated[UUID, Field(..., description="Уникальный идентификатор")]


class DeleteLearningTextResponse(BaseModel):
    """Данные, отправляемые в ответ на запрос удаления текста."""

    id: Annotated[UUID, Field(..., description="Уникальный идентификатор")]


class UpdateLearningTextRequest(BaseModel):
    """Данные, требующиеся для обновления данных о тексте."""

    title: Annotated[Optional[str], Field(max_length=100, description="Название")]
    difficulty: Annotated[Optional[int], Field(ge=0, le=10, description="Сложность")]
    preview: Annotated[Optional[str], Field(max_length=500, description="Краткое описание")]
    value: Annotated[Optional[str], Field(..., description="Содержание")]
    transcription: Annotated[Optional[str], Field(..., description="Транскрипционная запись")]


class UpdateLearningTextResponse(DetailLearningTextResponse):
    """Данные, отправляемые в ответ на запрос обновления данных о тексте."""
