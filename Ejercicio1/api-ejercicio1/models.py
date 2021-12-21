from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base #Se importa el objeto Base desde el archivo database.py

association_table = Table('cat', Base.metadata,
    Column('id_news', ForeignKey('news.id_news'), primary_key=True),
    Column('id_category', ForeignKey('has_category.id_category'), primary_key=True)
)

class News(Base): 

    __tablename__ = "news"

    id_news = Column(Integer, primary_key=True, index=True)
    id_category = Column(Integer, ForeignKey("has_category.id_category"))
    title = Column(String(150))
    date = Column(Date)
    url = Column(String(300))
    media_outlet = Column(String(100))

    category = relationship("Category", secondary = association_table, back_populates="news_cat")

class Category(Base):
	
    __tablename__ = "has_category"
	
    id_category = Column(Integer, primary_key=True,index=True)
    id_news = Column(Integer, ForeignKey("news.id_category"))
    value = Column(String(100))
	
    news_cat = relationship("News", secondary = association_table, back_populates="category")