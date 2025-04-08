from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from database.models import LearningText
from schemas.texts import (
    CreateLearningTextRequest,
    CreateLearningTextResponse,
    DeleteLearningTextResponse,
    DetailLearningTextResponse,
    LearningTextResponse,
)

router = APIRouter()


@router.get("/", summary="Получить список всех текстов")
async def get_texts(db: AsyncSession = Depends(get_db)) -> List[LearningTextResponse]:
    """Возвращает полный список всех обучающих текстов с краткой информацией."""
    stmt = select(LearningText)
    result = await db.execute(stmt)
    texts = result.scalars().all()

    return [LearningTextResponse.model_validate(text) for text in texts]


@router.get("/{uuid}", summary="Получить детальную информацию о тексте")
async def get_text(
    uuid: Annotated[UUID, Path(...)],
    db: AsyncSession = Depends(get_db),
) -> DetailLearningTextResponse:
    """Возвращает полную информацию о конкретном тексте по его UUID."""
    stmt = select(LearningText).where(LearningText.id == uuid)
    result = await db.execute(stmt)
    text = result.scalar_one_or_none()

    if text is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Text not found.",
        )

    return DetailLearningTextResponse.model_validate(text)


@router.post("/", summary="Добавить текст в систему")
async def create_text(
    data: Annotated[CreateLearningTextRequest, Body(...)],
    db: AsyncSession = Depends(get_db),
) -> CreateLearningTextResponse:
    """Добавляет новый текст в систему."""

    try:
        text = LearningText(
            title=data.title,
            difficulty=data.difficulty,
            preview=data.preview,
            value=data.value,
            transcription=data.transcription,
        )
        db.add(text)
        await db.commit()
        await db.refresh(text)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{LearningText.__name__} with this data already exists.",
        )

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error ocured while creating {LearningText.__name__}.",
        )

    return CreateLearningTextResponse.model_validate(text)


@router.delete("/{uuid}", summary="Удалить текст из системы")
async def delete_text(
    uuid: Annotated[UUID, Path(...)],
    db: AsyncSession = Depends(get_db),
) -> DeleteLearningTextResponse:
    """Удаляет текст из системы по его UUID."""
    stmt = select(LearningText).where(LearningText.id == uuid)
    result = await db.execute(stmt)
    text = result.scalar_one_or_none()

    if text is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Text not found.",
        )

    await db.delete(text)
    await db.commit()

    return DeleteLearningTextResponse.model_validate(text)
