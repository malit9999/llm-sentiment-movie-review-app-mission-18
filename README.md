# Bootcamp Mission 18 - 영화 리뷰 감성 분석 웹 애플리케이션

## 1. 개요
영화 정보, 사용자 리뷰, 리뷰 감성 분석 결과를 제공하는 Streamlit + FastAPI 기반 웹 애플리케이션 미션입니다.

## 2. 목표
프론트엔드, 백엔드, 데이터베이스, 감성 분석 모델을 연결한 AI 서비스 구조를 구현하는 것을 목표로 했습니다.

## 3. 사용 기술
- Python
- streamlit
- requests
- fastapi
- uvicorn
- SQLAlchemy
- pydantic
- transformers
- torch
- numpy
- pandas
- python-multipart

## 4. 주요 기능
- 영화 등록/조회/삭제
- 리뷰 등록 및 조회
- 리뷰 감성 분석
- Streamlit 프론트엔드
- FastAPI 백엔드 API

## 5. 실행 방법
```bash
pip install -r requirements.txt
cd backend
uvicorn main:app --reload
cd ../frontend
streamlit run app.py
```

## 6. 주요 파일
- `frontend/requirements.txt`
- `frontend/app.py`
- `backend/models.py`
- `backend/requirements.txt`
- `backend/sentiment.py`
- `backend/database.py`
- `backend/schemas.py`
- `backend/main.py`
- `images/영화 수정삭제.png`
- `images/영화별 리뷰.png`

## 7. 폴더 구조
```text
bootcamp-mission-18
  .gitignore
  backend/
    database.py
    main.py
    models.py
    requirements.txt
    schemas.py
    sentiment.py
  docs/
    mission18_report.pdf
  frontend/
    app.py
    requirements.txt
  images/
    리뷰 등록.png
    영화 등록.png
    영화 수정삭제.png
    영화별 리뷰.png
    통계 대시보드.png
    홈화면.png
  README.md
  requirements.txt
```

## 8. 학습 내용
AI 모델을 서비스 기능에 통합하고, 프론트엔드와 백엔드가 API로 통신하는 구조를 학습했습니다.

## 9. 트러블슈팅
미션을 진행하며 발생한 오류와 해결 과정은 노트북 또는 보고서에 정리했습니다.

## 10. 결과 화면
결과 이미지는 노트북 출력, 보고서 또는 `images/` 폴더에서 확인할 수 있습니다.

## 11. 공개 전 확인 사항
- frontend/.venv, backend/.venv, mission18.db는 공개 저장소 대상에서 제외했습니다.
- DB 파일은 실행 시 로컬에서 생성되는 방식으로 관리하는 것을 권장합니다.
