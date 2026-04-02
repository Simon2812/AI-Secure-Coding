from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    category = Column(String)


def list_articles(engine, category: str, offset: int, limit: int):
    with Session(engine) as session:
        stmt = (
            select(Article)
            .where(Article.category == category)
            .offset(offset)
            .limit(limit)
        )
        return session.execute(stmt).scalars().all()