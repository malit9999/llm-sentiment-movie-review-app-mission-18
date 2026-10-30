# Movie Review Sentiment Analysis App

> **Bootcamp Mission 18** | AI Backend and Web Service

## 미션 소개
영화 정보와 사용자 리뷰를 관리하고, 리뷰 작성 시 감성 분석 결과를 제공하는 Streamlit + FastAPI 기반 AI 웹 애플리케이션입니다. 프론트엔드·백엔드·데이터베이스·NLP 모델을 API 중심으로 연결했습니다.

## 구현 목표
- 영화와 리뷰를 관리하는 REST API를 구현한다.
- 리뷰 텍스트에 감성 분석 모델을 적용한다.
- Streamlit 화면에서 백엔드 API를 호출한다.
- 서비스 실행 흐름을 프론트엔드와 백엔드로 분리한다.

## 주요 구현 내용
- 영화 등록·조회·삭제
- 리뷰 등록·조회·삭제
- 리뷰 감성 분석과 평균 점수 조회
- FastAPI 자동 문서
- Streamlit 기반 사용자 화면

## 사용 기술
- Python
- FastAPI
- Streamlit
- SQLAlchemy
- Transformers
- PyTorch
- SQLite

## 실행 방법
```bash
pip install -r requirements.txt
# Terminal 1
cd backend
uvicorn main:app --reload
# Terminal 2
cd frontend
streamlit run app.py
```

> 데이터셋 또는 사전학습 모델이 외부에서 제공되는 경우, 실행 전에 노트북 또는 코드의 데이터 로드 설정을 확인해야 합니다.

## 폴더 구조
```text
frontend/  # Streamlit 사용자 화면
backend/   # FastAPI, DB 모델, 감성 분석 로직
images/    # 서비스 실행 화면
docs/      # 미션 보고서
```

## 학습 내용
- AI 모델 기능을 API 서비스에 연결하는 방법
- 프론트엔드와 백엔드의 책임을 분리하는 방법
- 로컬 DB와 모델 추론 자원을 관리하는 방법

## 트러블슈팅 및 재현 시 참고 사항
mission18.db와 가상환경은 .gitignore로 제외하며, 모델 다운로드 시간은 최초 실행 환경에 따라 달라질 수 있습니다.

## 결과 확인
서비스 화면은 images 폴더와 docs/mission18_report.pdf에서 확인할 수 있습니다.

## 포트폴리오 관점
이 저장소는 **AI Backend and Web Service** 역량을 학습·실험한 결과물입니다. 구현 범위와 실행 조건은 코드 및 노트북을 기준으로 확인할 수 있습니다.