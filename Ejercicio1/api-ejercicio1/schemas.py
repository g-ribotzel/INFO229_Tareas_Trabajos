from typing import List, Optional
import datetime
from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    url: str
    media_outlet: str
	

class NewsCreate(NewsBase):
    pass

class News(NewsBase):
    id_news: int
    id_category: int
    date : datetime.date

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    value: str
	
class CategoryCreate(CategoryBase):
	pass
	
class Category(CategoryBase):
    id_category: int
    id_news: int
	
    class Config:
        orm_mode = True

