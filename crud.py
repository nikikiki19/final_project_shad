# crud_seller.py
from sqlalchemy.orm import Session
from src.models.books import Seller  # Импорт модели Seller из modelbooks.py
from src.schemas.schemas_seller import SellerCreate, SellerUpdate  # Или где у вас лежат схемы
# Или, если у вас схемы Seller в общем файле schemas.py:
# from .schemas import SellerCreate, SellerUpdate

def create_seller(db: Session, seller: SellerCreate) -> Seller:
    db_seller = Seller(
        first_name=seller.first_name,
        last_name=seller.last_name,
        e_mail=seller.e_mail,
        password=seller.password,
    )
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller

def get_sellers(db: Session, skip: int = 0, limit: int = 100) -> list[Seller]:
    return db.query(Seller).offset(skip).limit(limit).all()

def get_seller(db: Session, seller_id: int) -> Seller | None:
    return db.query(Seller).filter(Seller.id == seller_id).first()

def update_seller(db: Session, db_seller: Seller, seller_update: SellerUpdate) -> Seller:
    if seller_update.first_name is not None:
        db_seller.first_name = seller_update.first_name
    if seller_update.last_name is not None:
        db_seller.last_name = seller_update.last_name
    if seller_update.e_mail is not None:
        db_seller.e_mail = seller_update.e_mail
    db.commit()
    db.refresh(db_seller)
    return db_seller

def delete_seller(db: Session, db_seller: Seller) -> None:
    db.delete(db_seller)
    db.commit()