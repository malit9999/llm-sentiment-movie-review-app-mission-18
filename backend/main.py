from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from database import Base, engine, SessionLocal
from models import Movie, Review
from schemas import (
    MovieCreate,
    MovieUpdate,
    MovieResponse,
    MovieRatingResponse,
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
    ReviewListResponse
)
from sentiment import analyze_sentiment


# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mission18 Movie Review API",
    description="영화 정보, 리뷰, 감성 분석을 관리하는 FastAPI 백엔드입니다.",
    version="0.3.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def review_to_response(review: Review):
    return {
        "id": review.id,
        "movie_id": review.movie_id,
        "movie_title": review.movie.title if review.movie else None,
        "author": review.author,
        "content": review.content,
        "user_rating": review.user_rating,
        "sentiment_label": review.sentiment_label,
        "sentiment_score": review.sentiment_score,
        "created_at": review.created_at
    }


@app.get(
    "/",
    summary="서버 상태 확인",
    description="FastAPI 백엔드 서버가 정상 실행 중인지 확인합니다."
)
def root():
    return {
        "message": "Mission18 backend is running"
    }


@app.post(
    "/movies",
    response_model=MovieResponse,
    status_code=status.HTTP_201_CREATED,
    summary="영화 등록",
    description="제목, 개봉일, 감독, 장르, 포스터 URL을 입력받아 영화를 등록합니다."
)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    movie_data = movie.model_dump()
    movie_data["title"] = movie_data["title"].strip()
    movie_data["director"] = movie_data["director"].strip()
    movie_data["genre"] = movie_data["genre"].strip()
    movie_data["poster_url"] = movie_data["poster_url"].strip()

    existing_movie = (
        db.query(Movie)
        .filter(func.lower(Movie.title) == movie_data["title"].lower())
        .first()
    )

    if existing_movie is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="같은 제목의 영화가 이미 등록되어 있습니다."
        )

    new_movie = Movie(**movie_data)

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    return new_movie


@app.get(
    "/movies",
    response_model=list[MovieResponse],
    summary="전체 영화 조회",
    description="등록된 전체 영화 목록을 조회합니다."
)
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).order_by(Movie.id.desc()).all()
    return movies


@app.get(
    "/movies/{movie_id}",
    response_model=MovieResponse,
    summary="특정 영화 조회",
    description="영화 ID를 기준으로 특정 영화 정보를 조회합니다."
)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 영화를 찾을 수 없습니다."
        )

    return movie


@app.delete(
    "/movies/{movie_id}",
    summary="특정 영화 삭제",
    description="영화 ID를 기준으로 특정 영화를 삭제합니다. 연결된 리뷰도 함께 삭제됩니다."
)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 영화를 찾을 수 없습니다."
        )

    db.delete(movie)
    db.commit()

    return {
        "message": f"movie_id={movie_id} 영화가 삭제되었습니다."
    }

@app.patch(
    "/movies/{movie_id}",
    response_model=MovieResponse,
    summary="특정 영화 수정",
    description="영화 ID를 기준으로 제목, 개봉일, 감독, 장르, 포스터 URL 정보를 수정합니다."
)
def update_movie(
    movie_id: int,
    movie_update: MovieUpdate,
    db: Session = Depends(get_db)
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 영화를 찾을 수 없습니다."
        )

    update_data = movie_update.model_dump(exclude_unset=True)

    for key in ["title", "director", "genre", "poster_url"]:
        if key in update_data and update_data[key] is not None:
            update_data[key] = update_data[key].strip()

    next_title = update_data.get("title", movie.title)
    duplicate_movie = (
        db.query(Movie)
        .filter(
            Movie.id != movie_id,
            func.lower(Movie.title) == next_title.lower()
        )
        .first()
    )

    if duplicate_movie is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="같은 제목의 영화가 이미 등록되어 있습니다."
        )

    for key, value in update_data.items():
        setattr(movie, key, value)

    db.commit()
    db.refresh(movie)

    return movie

@app.post(
    "/reviews",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="리뷰 등록",
    description="영화 ID, 작성자, 리뷰 내용을 입력받아 리뷰를 등록합니다."
)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == review.movie_id).first()

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="리뷰를 등록할 영화를 찾을 수 없습니다."
        )

    sentiment_result = analyze_sentiment(review.content, review.user_rating)
    
    new_review = Review(
        movie_id=review.movie_id,
        author=review.author,
        content=review.content,
        user_rating=review.user_rating,
        sentiment_label=sentiment_result["label"],
        sentiment_score=sentiment_result["score"]
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    new_review = (
        db.query(Review)
        .options(joinedload(Review.movie))
        .filter(Review.id == new_review.id)
        .first()
    )

    return review_to_response(new_review)


@app.get(
    "/reviews",
    response_model=ReviewListResponse,
    summary="리뷰 목록 조회",
    description="등록된 리뷰를 페이지 단위로 조회합니다. limit과 offset을 사용합니다."
)
def get_reviews(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    total_count = db.query(Review).count()

    reviews = (
        db.query(Review)
        .options(joinedload(Review.movie))
        .order_by(Review.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total_count": total_count,
        "limit": limit,
        "offset": offset,
        "reviews": [review_to_response(review) for review in reviews]
    }


@app.get(
    "/movies/{movie_id}/reviews",
    response_model=list[ReviewResponse],
    summary="특정 영화 리뷰 조회",
    description="영화 ID를 기준으로 해당 영화에 등록된 리뷰 목록을 조회합니다."
)
def get_reviews_by_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 영화를 찾을 수 없습니다."
        )

    reviews = (
        db.query(Review)
        .options(joinedload(Review.movie))
        .filter(Review.movie_id == movie_id)
        .order_by(Review.id.desc())
        .all()
    )

    return [review_to_response(review) for review in reviews]

@app.patch(
    "/reviews/{review_id}",
    response_model=ReviewResponse,
    summary="리뷰 수정",
    description="리뷰 ID를 기준으로 작성자와 리뷰 내용을 수정합니다. 리뷰 내용이 수정되면 감성 분석도 다시 실행됩니다."
)
def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    db: Session = Depends(get_db)
):
    review = (
        db.query(Review)
        .options(joinedload(Review.movie))
        .filter(Review.id == review_id)
        .first()
    )

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 리뷰를 찾을 수 없습니다."
        )

    update_data = review_update.model_dump(exclude_unset=True)

    if "author" in update_data and update_data["author"] is not None:
        review.author = update_data["author"]

    content_changed = "content" in update_data and update_data["content"] is not None
    rating_changed = (
        "user_rating" in update_data
        and update_data["user_rating"] is not None
    )

    if content_changed:
        review.content = update_data["content"]

    if rating_changed:
        review.user_rating = update_data["user_rating"]

    if content_changed or rating_changed:
        sentiment_result = analyze_sentiment(review.content, review.user_rating)
        review.sentiment_label = sentiment_result["label"]
        review.sentiment_score = sentiment_result["score"]

    db.commit()
    db.refresh(review)

    review = (
        db.query(Review)
        .options(joinedload(Review.movie))
        .filter(Review.id == review_id)
        .first()
    )

    return review_to_response(review)

@app.delete(
    "/reviews/{review_id}",
    summary="리뷰 삭제",
    description="리뷰 ID를 기준으로 특정 리뷰를 삭제합니다."
)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 리뷰를 찾을 수 없습니다."
        )

    db.delete(review)
    db.commit()

    return {
        "message": f"review_id={review_id} 리뷰가 삭제되었습니다."
    }

@app.get(
    "/movies/{movie_id}/rating",
    response_model=MovieRatingResponse,
    summary="특정 영화 평점 조회",
    description="특정 영화의 사용자 평점 평균과 감성 분석 점수 평균을 계산합니다."
)
def get_movie_rating(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 영화를 찾을 수 없습니다."
        )

    reviews = (
        db.query(Review)
        .filter(Review.movie_id == movie_id)
        .all()
    )

    if len(reviews) == 0:
        return {
            "movie_id": movie.id,
            "title": movie.title,
            "review_count": 0,
            "average_sentiment_score": None,
            "average_rating_5": None,
            "label_summary": "리뷰가 아직 없습니다."
        }

    user_ratings = [
        review.user_rating
        for review in reviews
        if review.user_rating is not None
    ]
    sentiment_scores = [
        review.sentiment_score
        for review in reviews
        if review.sentiment_score is not None
    ]

    average_rating_5 = (
        round(sum(user_ratings) / len(user_ratings), 2)
        if user_ratings
        else None
    )
    average_score = (
        sum(sentiment_scores) / len(sentiment_scores)
        if sentiment_scores
        else None
    )

    if average_score is None:
        label_summary = "리뷰가 아직 없습니다."
    elif average_score >= 0.7:
        label_summary = "positive"
    elif average_score <= 0.3:
        label_summary = "negative"
    else:
        label_summary = "neutral"

    return {
        "movie_id": movie.id,
        "title": movie.title,
        "review_count": len(reviews),
        "average_sentiment_score": (
            round(average_score, 3)
            if average_score is not None
            else None
        ),
        "average_rating_5": average_rating_5,
        "label_summary": label_summary
    }
