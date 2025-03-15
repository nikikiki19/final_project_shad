from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError

__all__ = ["IncomingBook", "ReturnedBook", "ReturnedAllbooks"]

# Базовый класс "Книги", содержащий поля, которые есть во всех наследниках.
class BaseBook(BaseModel):
    title: str
    author: str
    year: int
    seller_id: int  # добавлено: идентификатор продавца

# Класс для валидации входящих данных. Не содержит id, так как его присваивает БД.
class IncomingBook(BaseBook):
    pages: int = Field(
        default=150, alias="count_pages"
    )

    @field_validator("year")
    @staticmethod
    def validate_year(val: int):
        if val < 2020:
            raise PydanticCustomError("Validation error", "Year is too old!")
        return val

# Класс для возврата данных книги, включает id
class ReturnedBook(BaseBook):
    id: int
    pages: int

# Класс для возврата списка книг
class ReturnedAllbooks(BaseModel):
    books: list[ReturnedBook]