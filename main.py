from typing import List

import openai
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

import app.crud as crud
import app.models as models
import app.schemas as schemas
from app.database import SessionLocal

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 필요한 기능
# 라우터
# 1. 홈 화면을 위해 추천 와인 10개 던져주기 -> 트리톤 서버 사용해보기
# 2. 검색 기능에서 Body 로 orm_dta 받기

# 데이터베이스
# 1. 검섹 로그 저징


# Get one wine
@app.get("/wines/{wine_id}", status_code=200, response_model=schemas.Wine)
def read_wine(wine_id: int, db: Session = Depends(get_db)):
    wine: models.Wine = crud.get_wine_by_wine_id(db, wine_id)
    if wine is None:
        raise HTTPException(status_code=404, detail="To do not found")
    crud.update_count(db, wine)
    return wine


# Search wine
@app.post("/wines/search/{name}", status_code=200, response_model=List[schemas.Wine])
def search_wine_by_name(name: str, lang: str, db: Session = Depends(get_db)):
    if lang == "en":
        return crud.search_wine_by_en_name(db, name)
    return crud.get_wine_by_wine_name(db, name)


@app.post("/search/chat/{ocr}", status_code=200, response_model=List[schemas.Wine])
def ocr_search(db: Session = Depends(get_db)):
    return


# 상위 10개 와인데이터 불러오기
@app.get("/top/", status_code=200, response_model=List[schemas.Wine])
def top_ten(db: Session = Depends(get_db)):
    return db.query(models.Wine).order_by(desc(models.Wine.count)).limit(10).all()


@app.post("/gpt/")
def run_conversation(item: schemas.OcrItem, db: Session = Depends(get_db)):
    openai.organization = "org-ILi5zyGBnNlwVzZBJddFY8Nl"
    openai.api_key = "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"
    openai.Model.list()

    content = f"""
        \"""{item.ocr_text}\"""
        Exact wine product name without vintage
        Response format : "wine_name" only
    """
    messages = [{"role": "user", "content": content}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
    )
    response_message = response["choices"][0]["message"]

    message = response_message["content"]
    return crud.search_wine_by_en_name(db, message)

# 이름으로 와인 가져오기
# @app.get("/wines/{name}", status_code=200, response_model=schemas.Wine)
# def get_wine_ex_name(name: str, db: Session = Depends(get_db)):
#     wine: models.Wine = crud.get_wine_by_ex_name(db, name)
#     if wine is None:
#         raise HTTPException(status_code=404, detail="To do not found")
#     return wine

# ??
# @app.post("/wines/{name_en}", status_code=200, response_model=schemas.Wine)
# def answer_wine(name_en: str, db: Session = Depends(get_db)):
#     wine: models.Wine = crud.get_wine_by_wine_name(db, name_en)
#     if wine is None:
#         raise HTTPException(status_code=404, detail="To do not found")
#     return wine


# ??
# @app.post("/search/{name_en}", status_code=200, response_model=schemas.Wine)
# def search_wine(name_en: str, db: Session = Depends(get_db)):
#     return db.query(name_en)
