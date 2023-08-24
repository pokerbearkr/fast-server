from sqlalchemy import or_
from sqlalchemy.orm import Session

from sqlalchemy import desc

import app.models as models


# def get_wine_by_wine_id(db: Session, wine_id: int) -> models.Wine:
#    return db.scalar(select(models.Wine).select_from(db).where(models.Wine.wine_id == wine_id))


def get_wine_by_wine_id(db: Session, wine_id: int) -> models.Wine:
    return db.query(models.Wine).filter(models.Wine.wine_id == wine_id).first()


def get_wine_by_ex_name(db: Session, name: str):
    return db.query(models.Wine).filter(models.Wine.name_en == name).first()


# 한영 상관없이 검색하는 기능
def get_wine_by_wine_name(db: Session, name: str):
    return db.query(models.Wine).filter(
        or_(models.Wine.name_kr.like(f"%{name}%"), models.Wine.name_en.like(f"%{name}%"))).all()


# 영어로만 검색하는 기능
def search_wine_by_en_name(db: Session, name_en: str):
    return db.query(models.Wine).filter(models.Wine.name_en.like(f"%{name_en}%")).all()


# def wine_recommend(db:Session, name)

def update_count(db: Session, wine: models.Wine):
    wine.increase_count()
    db.add(wine)
    db.commit()
    db.refresh(wine)
