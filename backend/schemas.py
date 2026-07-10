from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


class MovieCreate(BaseModel):
    title: str
    release_date: date
    director: str
    genre: str
    poster_url: str


class MovieUpdate(BaseModel):
    title: str | None = None
    release_date: date | None = None
    director: str | None = None
    genre: str | None = None
    poster_url: str | None = None


class MovieResponse(BaseModel):
    id: int
    title: str
    release_date: date
    director: str
    genre: str
    poster_url: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReviewCreate(BaseModel):
    movie_id: int
    author: str
    content: str
    user_rating: float = Field(ge=1, le=5)


class ReviewUpdate(BaseModel):
    author: str | None = None
    content: str | None = None
    user_rating: float | None = Field(default=None, ge=1, le=5)


class ReviewResponse(BaseModel):
    id: int
    movie_id: int
    movie_title: str | None = None
    author: str
    content: str
    user_rating: float | None = None
    sentiment_label: str | None = None
    sentiment_score: float | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ReviewListResponse(BaseModel):
    total_count: int
    limit: int
    offset: int
    reviews: list[ReviewResponse]

class MovieRatingResponse(BaseModel):
    movie_id: int
    title: str
    review_count: int
    average_sentiment_score: float | None
    average_rating_5: float | None
    label_summary: str