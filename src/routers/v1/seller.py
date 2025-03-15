from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configurations import get_async_session
from src.models.books import Seller
from src.schemas.schemas_seller import SellerCreate, SellerRead, SellerReadWithBooks, SellerUpdate

# Зависимость для получения сессии БД
DBSession = Annotated[AsyncSession, Depends(get_async_session)]

router = APIRouter(prefix="/seller", tags=["seller"])

@router.post("/", response_model=SellerRead, status_code=status.HTTP_201_CREATED)
async def create_seller(seller: SellerCreate, session: DBSession):
    new_seller = Seller(
        first_name=seller.first_name,
        last_name=seller.last_name,
        e_mail=seller.e_mail,
        password=seller.password,  # на практике пароль нужно хэшировать!
    )
    session.add(new_seller)
    await session.flush()  # отправляем данные в БД, но не фиксируем коммит
    return new_seller

@router.get("/", response_model=List[SellerRead])
async def get_all_sellers(session: DBSession):
    query = select(Seller)
    result = await session.execute(query)
    sellers = result.scalars().all()
    return sellers

@router.get("/{seller_id}", response_model=SellerReadWithBooks)
async def get_seller(seller_id: int, session: DBSession):
    seller = await session.get(Seller, seller_id)
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
    return seller

@router.put("/{seller_id}", response_model=SellerRead)
async def update_seller(seller_id: int, update_data: SellerUpdate, session: DBSession):
    seller = await session.get(Seller, seller_id)
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
    if update_data.first_name is not None:
        seller.first_name = update_data.first_name
    if update_data.last_name is not None:
        seller.last_name = update_data.last_name
    if update_data.e_mail is not None:
        seller.e_mail = update_data.e_mail
    await session.flush()
    return seller

@router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller(seller_id: int, session: DBSession):
    seller = await session.get(Seller, seller_id)
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
    await session.delete(seller)
    await session.flush()
    return Response(status_code=status.HTTP_204_NO_CONTENT)