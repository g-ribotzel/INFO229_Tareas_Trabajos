from typing import List, Union, Optional, Dict

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
		

@app.get("/news/{cat}", response_model = List[Union[schemas.News, schemas.Category]])
def read_news_by_category_and_date(start: str, end: str, cat: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
	news = crud.get_news_by_category_date(db, cat=cat, start=start, end=end, skip=skip, limit=limit)
	return news

@app.get("/news/", response_model=List[schemas.News])
def read_news(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    news = crud.get_manyNews(db, skip=skip, limit=limit)
    return news


@app.get("/news/{id_news}", response_model=schemas.News)
def read_new(id_news: int, db: Session = Depends(get_db)):
    db_news = crud.get_news(db, id_news=id_news)
    if db_news is None:
        raise HTTPException(status_code=404, detail="News article not found")
    return db_news


@app.get("/category/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories
	