# src/schemas_seller.py

from pydantic import BaseModel, EmailStr
from typing import List, Optional

#
# Базовая схема (общие поля)
#
class SellerBase(BaseModel):
    first_name: str
    last_name: str
    e_mail: EmailStr

#
# Схема для создания (включает пароль)
#
class SellerCreate(SellerBase):
    password: str

#
# Схема для чтения (отдачи) продавца (без пароля!)
#
class SellerRead(SellerBase):
    id: int

    class Config:
        orm_mode = True

#
# Схема для обновления (пароль не трогаем)
#
class SellerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    e_mail: Optional[EmailStr] = None

#
# Доп. схема для "продавец + список книг"
#
from src.schemas import ReturnedBook  # или где у вас описана схема книги для ответа

class SellerReadWithBooks(SellerRead):
    # Включаем список книг (можно переиспользовать вашу ReturnedBook)
    books: List[ReturnedBook] = []

    class Config:
        orm_mode = True