from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from database.models import LearningText
from schemas import (
    CreateLearningTextRequest,
    CreateLearningTextResponse,
    DeleteLearningTextResponse,
    DetailLearningTextResponse,
    LearningTextResponse,
    UpdateLearningTextRequest,
    UpdateLearningTextResponse,
)
from service_logging import logger

from .utils.pagination import PaginatedResponse, Pagination

router = APIRouter()


@router.get("/", summary="Получить список всех текстов")
async def get_texts(
    pg: Annotated[Pagination, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PaginatedResponse[LearningTextResponse]:
    """Постранично возвращает список всех обучающих текстов."""
    logger.info("Getting the text list...")
    stmt = select(LearningText).offset(pg.skip).limit(pg.size)
    result = await db.execute(stmt)
    texts = result.scalars().all()

    stmt = select(func.count()).select_from(LearningText)
    result = await db.execute(stmt)
    total = result.scalar_one()

    items = [LearningTextResponse.model_validate(text) for text in texts]
    logger.success(f"Received {len(items)} texts.")

    return PaginatedResponse[LearningTextResponse](
        items=items,
        page=pg.page,
        size=pg.size,
        total=total,
    )


@router.get("/{uuid}", summary="Получить детальную информацию о тексте")
async def get_text(
    uuid: Annotated[UUID, Path(...)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DetailLearningTextResponse:
    """Возвращает полную информацию о конкретном тексте по его UUID."""
    logger.info("Getting information about a text...")
    stmt = select(LearningText).where(LearningText.id == uuid)
    result = await db.execute(stmt)
    text = result.scalar_one_or_none()

    if text is None:
        detail = "Text not found."
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )

    item = DetailLearningTextResponse.model_validate(text)
    logger.success(f"Text received: {item.id}")

    return item


@router.post("/", summary="Добавить текст в систему")
async def create_text(
    data: Annotated[CreateLearningTextRequest, Body(...)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> CreateLearningTextResponse:
    """Добавляет новый текст в систему."""
    logger.info("Creating a text...")
    try:
        text = LearningText(
            title=data.title,
            value=data.value,
            transcription=data.transcription,
        )
        db.add(text)
        await db.commit()
        await db.refresh(text)

    except IntegrityError:
        await db.rollback()
        detail = "Text with this data already exists."
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )

    except Exception as error:
        await db.rollback()
        detail = f"An error ocured while creating text: {error}"
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )

    item = CreateLearningTextResponse.model_validate(text)
    logger.success(f"Text has been created: {item.id}")

    return item


@router.delete("/{uuid}", summary="Удалить текст из системы")
async def delete_text(
    uuid: Annotated[UUID, Path(...)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeleteLearningTextResponse:
    """Удаляет текст из системы по его UUID."""
    logger.info("Deleting a text...")
    stmt = select(LearningText).where(LearningText.id == uuid)
    result = await db.execute(stmt)
    text = result.scalar_one_or_none()

    if text is None:
        detail = "Text not found."
        logger.error()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )

    await db.delete(text)
    await db.commit()

    item = DeleteLearningTextResponse.model_validate(text)
    logger.success(f"Text has been deleted: {item.id}")

    return item


@router.patch("/{uuid}", summary="Обновить данные о тексте")
async def update_text(
    uuid: Annotated[UUID, Path(...)],
    data: Annotated[UpdateLearningTextRequest, Body(...)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UpdateLearningTextResponse:
    """Обновляет данные текста по его UUID."""
    logger.info("Updating a text...")
    stmt = select(LearningText).where(LearningText.id == uuid)
    result = await db.execute(stmt)
    text = result.scalar_one_or_none()

    if text is None:
        detail = "Text not found."
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )

    try:
        data = data.model_dump(exclude_none=True)
        for field in data:
            setattr(text, field, data[field])

        db.add(text)
        await db.commit()
        await db.refresh(text)

    except IntegrityError:
        await db.rollback()
        detail = "Text with this data already exists."
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )

    except Exception as error:
        await db.rollback()
        detail = f"An error ocured while updating text: {error}"
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )

    item = UpdateLearningTextResponse.model_validate(text)
    logger.success(f"Text has been updated: {item.id}")

    return item
