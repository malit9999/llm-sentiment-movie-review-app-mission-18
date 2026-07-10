from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    release_date = Column(Date, nullable=False)
    director = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    poster_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    reviews = relationship(
        "Review",
        back_populates="movie",
        cascade="all, delete-orphan"
    )


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    author = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_rating = Column(Float, nullable=True)

    # v0.4 감성분석 단계에서 사용할 컬럼입니다.
    sentiment_label = Column(String, nullable=True)
    sentiment_score = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    movie = relationship("Movie", back_populates="reviews")
    