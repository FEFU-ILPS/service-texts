from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import Column, String
from sqlalchemy import BinaryExpression


def build_search_condition(
    column: Column,
    operator: str,
    search_value: str | int | float | date,
) -> BinaryExpression:
    """Функция строит выражение для поиска по значению.

    Функция принимает на вход колонку таблицы, символ оператора и значение,
    после чего строит бинарное выражение для сравнения значения колонки с переданым
    значением через оператор.

    Args:
        column (Column): Колонка таблицы SQLAlchemy.
        operator (str): Символ применяемого оператора.
        search_value (str | int | float | date): Значение для сравнения.

    Raises:
        HTTPException: 400. Несовпадение типа колонки и оператора поиска.

    Returns:
        BinaryExpression: SQLAlchemy выражение для поиска.
    """
    if operator == "ILIKE":
        if not isinstance(column.type, String):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot use this search mode on non-string field",
            )
        return getattr(column, operator.lower())(f"%{search_value}%")

    elif operator != "=" and isinstance(column.type, String):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot use this search mode on non-numeric field",
        )

    elif operator in ("<", ">", "<=", ">=") and isinstance(search_value, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot use this search mode with non-numeric or non-date search value",
        )

    return column.op(operator)(search_value)
