from sqlalchemy import update
from sqlalchemy.orm import Session

import models
import schemas


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def put_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db_item.id = item_id
    db.execute(update(models.Item), [{"id": item_id, **item.model_dump()}])
    db.commit()

    return db_item