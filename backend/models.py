from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    review = Column(String)

    sentiment = Column(String)

    confidence = Column(Float)

    fake = Column(Boolean)