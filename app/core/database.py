from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker


# Create an in-memory SQLite database for demo purposes
engine = create_engine("sqlite:///cfb.db", echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
