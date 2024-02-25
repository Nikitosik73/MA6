from sqlalchemy import create_engine, String, UUID, Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'

engine = create_engine(URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_paramonov'

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String)
    second_name = Column(String)
    dick_size = Column(Integer)