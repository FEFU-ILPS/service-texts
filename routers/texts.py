from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from database.models import LearningText
from schemas.texts import LearningTextResponse, DetailLearningTextResponse

router = APIRouter()


@router.get("", summary="Получить список всех текстов")
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
