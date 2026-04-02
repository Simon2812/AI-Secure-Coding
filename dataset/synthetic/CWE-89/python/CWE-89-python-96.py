from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String)


def get_user(engine, email: str):
    with Session(engine) as session:
        stmt = select(User).where(User.email == email)
        return session.execute(stmt).scalar_one_or_none()


if __name__ == "__main__":
    engine = create_engine("sqlite:///app.db")
    user = get_user(engine, "a@b.com")
    _ = user