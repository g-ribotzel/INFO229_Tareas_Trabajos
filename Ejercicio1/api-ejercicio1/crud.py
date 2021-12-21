from sqlalchemy.orm  import Session
from . import models, schemas

def get_news(db: Session, id_news: int):
	return db.query(models.News).filter(models.News.id_news == id_news).first()
	
def get_news_by_media(db: Session, media: str):
	return db.query(models.News).filter(models.News.media_outlet == media).first()
	
def get_manyNews(db: Session, skip: int = 0, limit: int = 100):
	return db.query(models.News).offset(skip).limit(limit).all()
	
def get_categories(db:Session, skip: int=0, limit: int=100):
	return db.query(models.Category).offset(skip).limit(limit).all()
	
def get_category_by_tag(db:Session, cat: str , skip: int=0, limit: int=100):
	return db.query(models.Category).filter(models.Category.value.contains(cat)).offset(skip).limit(limit).all()

def get_news_by_category(db:Session, cat: str, skip: int=0, limit: int=100):
	return db.query(models.News).join(models.Category, models.News.id_news == models.Category.id_news).filter(models.Category.value.contains(cat)).offset(skip).limit(limit).all()
	
def get_news_by_category_date(db:Session, cat: str, start: str, end: str, skip: int=0, limit: int=100):
	return db.query(models.News).join(models.Category, models.News.id_news == models.Category.id_news).filter(models.Category.value.contains(cat)).filter(models.News.date.between(start,end)).offset(skip).limit(limit).all()