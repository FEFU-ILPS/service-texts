from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LearningTextResponse(BaseModel):
    """Данные, отправляемые в ответ на запрос получения всех текстов."""

    model_config = ConfigDict(from_attributes=True)

    id: Annotated[
        UUID,
        Field(
            description="Уникальный идентификатор",
            examples=[
                "d08191a1-3a4f-48e3-be3b-fc3bb31536af",
                "3d5dc460-5db7-4dd0-9d4e-3cd825ebaebd",
            ],
        ),
    ]
    title: Annotated[
        str,
        Field(
            max_length=100,
            description="Название",
            examples=[
                "Моя прекрасная жизнь",
                "Как я провел лето",
                "История великого русского государства",
            ],
        ),
    ]
    difficulty: Annotated[
        Optional[int],
        Field(
            ge=0,
            le=10,
            description="Сложность",
            default=0,
            examples=[0, 1, 2, 3, 4, 5],
        ),
    ]
    preview: Annotated[
        Optional[str],
        Field(
            max_length=500,
            description="Краткое описание",
            examples=[
                "Этот текст повествует трагичную историю деда Максима",
                "В этом рассказе раскрываются ноты человеческой души",
            ],
        ),
    ]


class DetailLearningTextResponse(LearningTextResponse):
    """Данные, отправляемые в ответ на запрос получения деталей о тексте."""

    value: Annotated[
        str,
        Field(
            description="Содержание",
            examples=[
                (
                    "School later when imagine. Push effort consider shoulder.\n"
                    "Meet institution yes tend. Check order food reach wait friend.\n"
                    "Real stop scientist heart window safe."
                ),
                (
                    "Third president billion measure. Same player government check can business. "
                    "Kitchen like develop admit most.\nLight red writer. Others field as pressure "
                    "question movement ask pretty."
                ),
            ],
        ),
    ]
    transcription: Annotated[
        str,
        Field(
            description="Транскрипционная запись",
            examples=[
                "Dɑːɹk hæd hæd jɚ jɚ ʃi suːt suːt ʃi hæd jɚ jɚ ʃi",
                "hæd suːt jɚ jɚ ʃi dɑːɹk ʃi hæd ʃi dɑːɹk ʃi hæd hæd hæd suːt jɚ suːt",
            ],
        ),
    ]


class CreateLearningTextRequest(BaseModel):
    """Данные, требующиеся для создания/добавления текста в систему."""

    title: Annotated[
        str,
        Field(
            max_length=100,
            description="Название",
            examples=[
                "Моя прекрасная жизнь",
                "Как я провел лето",
                "История великого русского государства",
            ],
        ),
    ]
    difficulty: Annotated[
        Optional[int],
        Field(
            ge=0,
            le=10,
            description="Сложность",
            default=0,
            examples=[0, 1, 2, 3, 4, 5],
        ),
    ]
    preview: Annotated[
        Optional[str],
        Field(
            max_length=500,
            description="Краткое описание",
            examples=[
                "Этот текст повествует трагичную историю деда Максима",
                "В этом рассказе раскрываются ноты человеческой души",
            ],
        ),
    ]
    value: Annotated[
        str,
        Field(
            description="Содержание",
            examples=[
                (
                    "School later when imagine. Push effort consider shoulder.\n"
                    "Meet institution yes tend. Check order food reach wait friend.\n"
                    "Real stop scientist heart window safe."
                ),
                (
                    "Third president billion measure. Same player government check can business. "
                    "Kitchen like develop admit most.\nLight red writer. Others field as pressure "
                    "question movement ask pretty."
                ),
            ],
        ),
    ]
    # TODO: Разработать алгоритм, позволяющий создать default factory преобразования текста в транскрипцию
    # ! Позже можно сделать Optional
    transcription: Annotated[
        str,
        Field(
            description="Транскрипционная запись",
            examples=[
                "Dɑːɹk hæd hæd jɚ jɚ ʃi suːt suːt ʃi hæd jɚ jɚ ʃi",
                "hæd suːt jɚ jɚ ʃi dɑːɹk ʃi hæd ʃi dɑːɹk ʃi hæd hæd hæd suːt jɚ suːt",
            ],
        ),
    ]


class CreateLearningTextResponse(BaseModel):
    """Данные, отправляемые в ответ на запрос добавления текста."""

    model_config = ConfigDict(from_attributes=True)

    id: Annotated[
        UUID,
        Field(
            description="Уникальный идентификатор",
            examples=[
                "d08191a1-3a4f-48e3-be3b-fc3bb31536af",
                "3d5dc460-5db7-4dd0-9d4e-3cd825ebaebd",
            ],
        ),
    ]


class DeleteLearningTextResponse(BaseModel):
    """Данные, отправляемые в ответ на запрос удаления текста."""

    model_config = ConfigDict(from_attributes=True)

    id: Annotated[
        UUID,
        Field(
            description="Уникальный идентификатор",
            examples=[
                "d08191a1-3a4f-48e3-be3b-fc3bb31536af",
                "3d5dc460-5db7-4dd0-9d4e-3cd825ebaebd",
            ],
        ),
    ]


class UpdateLearningTextRequest(BaseModel):
    """Данные, требующиеся для обновления данных о тексте."""

    title: Annotated[
        Optional[str],
        Field(
            max_length=100,
            description="Название",
            examples=[
                "Моя прекрасная жизнь",
                "Как я провел лето",
                "История великого русского государства",
            ],
            default=None,
        ),
    ]
    difficulty: Annotated[
        Optional[int],
        Field(
            ge=0,
            le=10,
            description="Сложность",
            examples=[0, 1, 2, 3, 4, 5],
            default=None,
        ),
    ]
    preview: Annotated[
        Optional[str],
        Field(
            max_length=500,
            description="Краткое описание",
            examples=[
                "Этот текст повествует трагичную историю деда Максима",
                "В этом рассказе раскрываются ноты человеческой души",
            ],
            default=None,
        ),
    ]
    value: Annotated[
        Optional[str],
        Field(
            description="Содержание",
            examples=[
                (
                    "School later when imagine. Push effort consider shoulder.\n"
                    "Meet institution yes tend. Check order food reach wait friend.\n"
                    "Real stop scientist heart window safe."
                ),
                (
                    "Third president billion measure. Same player government check can business. "
                    "Kitchen like develop admit most.\nLight red writer. Others field as pressure "
                    "question movement ask pretty."
                ),
            ],
            default=None,
        ),
    ]
    # TODO: Разработать алгоритм, позволяющий создать default factory преобразования текста в транскрипцию
    # ! Позже можно сделать Optional
    transcription: Annotated[
        Optional[str],
        Field(
            description="Транскрипционная запись",
            examples=[
                "Dɑːɹk hæd hæd jɚ jɚ ʃi suːt suːt ʃi hæd jɚ jɚ ʃi",
                "hæd suːt jɚ jɚ ʃi dɑːɹk ʃi hæd ʃi dɑːɹk ʃi hæd hæd hæd suːt jɚ suːt",
            ],
            default=None,
        ),
    ]


class UpdateLearningTextResponse(DetailLearningTextResponse):
    """Данные, отправляемые в ответ на запрос обновления данных о тексте."""
