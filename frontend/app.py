import os
import calendar
import json
import time
from urllib.parse import urlparse
import requests
import streamlit as st
import streamlit.components.v1 as components
from datetime import date, datetime

APP_VERSION = "frontend_v0_1_basic_streamlit"

# 로컬 개발 기본 주소
# Streamlit Cloud 배포 시에는 환경변수 BACKEND_URL로 교체 가능
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


st.set_page_config(
    page_title="CineScope",
    page_icon="CS",
    layout="wide"
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1180px;
    }

    div[data-testid="stAppViewContainer"] {
        background: #f7f8fb;
    }

    h1, h2, h3 {
        letter-spacing: 0;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e8ecf3;
        border-radius: 8px;
        padding: 0.9rem 1rem;
    }

    .cinescope-hero {
        display: grid;
        grid-template-columns: minmax(0, 1.15fr) minmax(280px, 0.85fr);
        gap: 1.5rem;
        align-items: stretch;
        margin-bottom: 1.5rem;
    }

    .cinescope-hero-main {
        background: #ffffff;
        border: 1px solid #e8ecf3;
        border-radius: 8px;
        padding: 2rem;
        box-shadow: 0 16px 42px rgba(31, 41, 55, 0.08);
    }

    .cinescope-kicker {
        color: #d42b3a;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 0.65rem;
    }

    .cinescope-home-link {
        display: inline-block;
        color: inherit;
        text-decoration: none;
        cursor: pointer;
    }

    .cinescope-home-link:hover,
    .cinescope-home-link:focus {
        color: inherit;
        text-decoration: none;
    }

    .cinescope-home-link:focus-visible {
        outline: 3px solid rgba(212, 43, 58, 0.35);
        outline-offset: 6px;
        border-radius: 8px;
    }

    .cinescope-home-link:hover .cinescope-title {
        color: #d42b3a;
    }

    .cinescope-title {
        color: #202633;
        font-size: 3rem;
        line-height: 1.05;
        font-weight: 800;
        margin-bottom: 0.85rem;
    }

    .cinescope-copy {
        color: #596273;
        font-size: 1.05rem;
        line-height: 1.65;
        max-width: 680px;
    }

    .cinescope-panel {
        background: #202633;
        border-radius: 8px;
        padding: 1.5rem;
        color: #ffffff;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 220px;
    }

    .cinescope-panel-title {
        font-size: 1.15rem;
        font-weight: 750;
        margin-bottom: 0.6rem;
    }

    .cinescope-panel-copy {
        color: #cfd6e4;
        line-height: 1.55;
        font-size: 0.95rem;
    }

    .section-heading {
        display: flex;
        justify-content: space-between;
        align-items: end;
        gap: 1rem;
        margin: 1rem 0 0.75rem;
    }

    .section-heading h2 {
        margin: 0;
        color: #202633;
        font-size: 1.55rem;
    }

    .section-heading p {
        margin: 0.3rem 0 0;
        color: #6b7280;
        font-size: 0.95rem;
    }

    .featured-card-wrap {
        border: 1px solid #e8ecf3;
        border-radius: 8px;
        padding: 0.95rem;
        min-height: 100%;
        box-shadow: 0 12px 32px rgba(31, 41, 55, 0.06);
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.featured-card-marker) {
        position: relative;
        border-radius: 8px;
        border: 1px solid #e8ecf3;
        box-shadow: 0 12px 32px rgba(31, 41, 55, 0.06);
        overflow: hidden;
    }

    div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .theme-0.featured-card-marker),
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.theme-0.featured-card-marker) {
        background: linear-gradient(180deg, #ffd4dc 0%, #ffe8ec 100%) !important;
        border-color: #ef9aa6;
    }

    div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .theme-1.featured-card-marker),
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.theme-1.featured-card-marker) {
        background: linear-gradient(180deg, #cde5ff 0%, #e8f4ff 100%) !important;
        border-color: #91c4f5;
    }

    div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .theme-2.featured-card-marker),
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.theme-2.featured-card-marker) {
        background: linear-gradient(180deg, #d1efd8 0%, #eaf8ed 100%) !important;
        border-color: #96d5a4;
    }

    div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .featured-card-marker) > div[data-testid="stElementContainer"],
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.featured-card-marker) [data-testid="stVerticalBlock"] {
        background: transparent !important;
        gap: 0.65rem;
    }

    .featured-card-marker {
        display: none;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.featured-card-marker) > div {
        position: relative;
        z-index: 1;
    }

    .featured-card-wrap.theme-0 {
        background: #ffd9df;
    }

    .featured-card-wrap.theme-1 {
        background: #d7eaff;
    }

    .featured-card-wrap.theme-2 {
        background: #daf3df;
    }

    .recommend-reason {
        background: transparent;
        border: 0;
        border-radius: 0;
        padding: 0.15rem 0 0.55rem;
        margin-bottom: 0.35rem;
        color: #202633;
        text-align: center;
        box-shadow: none;
    }

    .recommend-reason-text {
        font-size: 0.98rem;
        line-height: 1.35;
        font-weight: 850;
    }

    .recommend-reason.theme-0 .recommend-reason-text {
        color: #c92635;
    }

    .recommend-reason.theme-1 .recommend-reason-text {
        color: #2563a8;
    }

    .recommend-reason.theme-2 .recommend-reason-text {
        color: #287a44;
    }

    .movie-card {
        background: #ffffff;
        border: 1px solid #e8ecf3;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 10px 30px rgba(31, 41, 55, 0.06);
        min-height: 100%;
    }

    .movie-card img {
        border-radius: 6px;
    }

    .movie-meta {
        color: #6b7280;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    .movie-score-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.55rem;
        margin-top: 0.75rem;
    }

    .movie-score {
        background: #f3f5f9;
        border-radius: 8px;
        padding: 0.65rem;
    }

    .movie-score-label {
        color: #6b7280;
        font-size: 0.78rem;
        margin-bottom: 0.1rem;
    }

    .movie-score-value {
        color: #202633;
        font-size: 1rem;
        font-weight: 750;
    }

    div[data-testid="stDialog"] div[role="dialog"] {
        position: fixed !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
    }

    @media (max-width: 860px) {
        .cinescope-hero {
            grid-template-columns: 1fr;
        }

        .cinescope-title {
            font-size: 2.25rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


def request_get(path: str, params: dict | None = None):
    try:
        response = requests.get(
            f"{BACKEND_URL}{path}",
            params=params,
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        st.error(f"API 요청 실패: {error}")
        return None


def request_post(path: str, payload: dict):
    try:
        response = requests.post(
            f"{BACKEND_URL}{path}",
            json=payload,
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        detail = None
        if getattr(error, "response", None) is not None:
            try:
                detail = error.response.json().get("detail")
            except ValueError:
                detail = error.response.text
        st.error(f"API 요청 실패: {detail or error}")
        return None

def request_patch(path: str, payload: dict):
    try:
        response = requests.patch(
            f"{BACKEND_URL}{path}",
            json=payload,
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        detail = None
        if getattr(error, "response", None) is not None:
            try:
                detail = error.response.json().get("detail")
            except ValueError:
                detail = error.response.text
        st.error(f"API 요청 실패: {detail or error}")
        return None

def request_delete(path: str):
    try:
        response = requests.delete(
            f"{BACKEND_URL}{path}",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        st.error(f"API 요청 실패: {error}")
        return None


def get_movies():
    movies = request_get("/movies")
    return movies if movies is not None else []


def get_reviews_page(limit: int = 10, offset: int = 0):
    data = request_get(
        "/reviews",
        params={
            "limit": limit,
            "offset": offset
        }
    )

    if data is None:
        return {
            "total_count": 0,
            "limit": limit,
            "offset": offset,
            "reviews": []
        }

    return data

def get_all_reviews():
    all_reviews = []
    limit = 100
    offset = 0

    while True:
        data = get_reviews_page(limit=limit, offset=offset)

        reviews = data.get("reviews", [])
        total_count = data.get("total_count", 0)

        all_reviews.extend(reviews)

        offset += limit

        if offset >= total_count:
            break

    return all_reviews


def safe_average(values):
    valid_values = [
        value for value in values
        if value is not None
    ]

    if not valid_values:
        return None

    return sum(valid_values) / len(valid_values)

def get_reviews_by_movie(movie_id: int):
    reviews = request_get(f"/movies/{movie_id}/reviews")

    if reviews is None:
        return []

    return reviews

def get_movie_rating(movie_id: int):
    return request_get(f"/movies/{movie_id}/rating")


def render_sentiment_badge(label: str | None):
    if label == "positive":
        return "긍정"
    if label == "negative":
        return "부정"
    if label == "neutral":
        return "중립"
    return "분석 전"


def format_user_rating(value):
    if value is None:
        return "평점 없음"

    return f"{float(value):.1f} / 5.0"


def format_sentiment_score(value):
    if value is None:
        return "점수 없음"

    return f"{float(value):.2f}"


def is_valid_image_url(value: str | None):
    if not value:
        return False

    parsed_url = urlparse(value.strip())
    return parsed_url.scheme in {"http", "https"} and bool(parsed_url.netloc)


def render_poster_image(poster_url: str | None, *, use_info: bool = True):
    if not is_valid_image_url(poster_url):
        message = "포스터 URL이 올바르지 않습니다." if poster_url else "포스터 없음"

        if use_info:
            st.info(message)
        else:
            st.write(message)

        return

    try:
        st.image(poster_url.strip(), use_container_width=True)
    except Exception:
        if use_info:
            st.info("포스터 이미지를 불러올 수 없습니다.")
        else:
            st.write("포스터 이미지를 불러올 수 없습니다.")


def navigate_to(page_name: str):
    st.session_state.pending_page = page_name
    st.rerun()


def get_featured_movies(movies: list[dict]):
    movie_cards = []

    for movie in movies:
        rating = get_movie_rating(movie["id"]) or {}
        movie_cards.append(
            {
                "movie": movie,
                "rating": rating,
                "review_count": rating.get("review_count") or 0,
                "average_rating": rating.get("average_rating_5") or 0,
                "recent_id": movie.get("id") or 0
            }
        )

    featured_cards = []
    used_movie_ids = set()

    sort_rules = [
        ("review_count", "리뷰가 가장 많은 영화"),
        ("average_rating", "평점이 가장 높은 영화"),
        ("recent_id", "가장 최근에 등록된 영화")
    ]

    for sort_key, reason in sort_rules:
        candidates = [
            card for card in movie_cards
            if card["movie"]["id"] not in used_movie_ids
        ]

        if not candidates:
            break

        selected_card = max(
            candidates,
            key=lambda item: (
                item[sort_key],
                item["review_count"],
                item["average_rating"],
                item["recent_id"]
            )
        )
        selected_card["recommend_reason"] = reason
        featured_cards.append(selected_card)
        used_movie_ids.add(selected_card["movie"]["id"])

    return featured_cards


def get_recommend_reason(card: dict, index: int):
    return card.get("recommend_reason", "추천 영화")


def render_movie_card(card: dict, index: int):
    movie = card["movie"]
    rating = card["rating"]
    average_rating = rating.get("average_rating_5")
    review_count = rating.get("review_count") or 0
    sentiment_label = rating.get("label_summary")

    reason = get_recommend_reason(card, index)

    with st.container(border=True):
        st.markdown(
            f"""
            <span class="featured-card-marker theme-{index % 3}"></span>
            <div class="recommend-reason theme-{index % 3}">
                <div class="recommend-reason-text">{reason}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        render_poster_image(movie.get("poster_url"))

        st.markdown(f"### {movie['title']}")
        st.markdown(
            f"""
            <div class="movie-meta">
                개봉일: {movie['release_date']}<br>
                감독: {movie['director']}<br>
                장르: {movie['genre']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="movie-score-row">
                <div class="movie-score">
                    <div class="movie-score-label">사용자 평점</div>
                    <div class="movie-score-value">{format_user_rating(average_rating)}</div>
                </div>
                <div class="movie-score">
                    <div class="movie-score-label">리뷰 수</div>
                    <div class="movie-score-value">{review_count}개</div>
                </div>
            </div>
            <div class="movie-score" style="margin-top: 0.55rem;">
                <div class="movie-score-label">대표 감성</div>
                <div class="movie-score-value">{render_sentiment_badge(sentiment_label)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col_review, col_write = st.columns(2)

        with col_review:
            if st.button(
                "리뷰 보기",
                key=f"featured_review_{movie['id']}_{index}",
                use_container_width=True
            ):
                st.session_state.movie_reviews_selected_id = movie["id"]
                navigate_to("영화별 리뷰")

        with col_write:
            if st.button(
                "리뷰 작성",
                key=f"featured_write_{movie['id']}_{index}",
                use_container_width=True,
                type="primary"
            ):
                st.session_state.review_create_selected_movie_id = movie["id"]
                navigate_to("리뷰 등록")


def movie_option_label(movie: dict):
    return f"ID{movie['id']} : {movie['title']}"


def render_selected_movie_preview(movie: dict):
    with st.container(border=True):
        col_poster, col_info = st.columns([1, 3])

        with col_poster:
            render_poster_image(movie.get("poster_url"))

        with col_info:
            st.markdown(f"### {movie['title']}")
            st.write(f"개봉일: {movie['release_date']}")
            st.write(f"감독: {movie['director']}")
            st.write(f"장르: {movie['genre']}")


def inject_selectbox_poster_hover(movies: list[dict]):
    poster_data = {
        movie_option_label(movie): {
            "title": movie["title"],
            "poster_url": (
                movie.get("poster_url", "").strip()
                if is_valid_image_url(movie.get("poster_url"))
                else ""
            )
        }
        for movie in movies
    }

    poster_json = json.dumps(poster_data, ensure_ascii=False).replace("</", "<\\/")

    components.html(
        f"""
        <script>
        (function() {{
            const parentWindow = window.parent;
            const parentDocument = parentWindow.document;
            parentWindow.__cinescopePosterPreviewData = {poster_json};

            function ensurePreview() {{
                let preview = parentDocument.getElementById("cinescope-selectbox-poster-preview");

                if (!preview) {{
                    preview = parentDocument.createElement("div");
                    preview.id = "cinescope-selectbox-poster-preview";
                    preview.style.position = "fixed";
                    preview.style.zIndex = "2147483647";
                    preview.style.display = "none";
                    preview.style.pointerEvents = "none";
                    preview.style.width = "150px";
                    preview.style.padding = "8px";
                    preview.style.background = "#ffffff";
                    preview.style.border = "1px solid #d9dee8";
                    preview.style.borderRadius = "8px";
                    preview.style.boxShadow = "0 18px 44px rgba(31, 41, 55, 0.24)";
                    preview.style.color = "#202633";
                    preview.style.fontSize = "12px";
                    parentDocument.body.appendChild(preview);
                }}

                return preview;
            }}

            function findLabel(text) {{
                const value = (text || "").trim();
                const data = parentWindow.__cinescopePosterPreviewData || {{}};

                return Object.keys(data).find(function(label) {{
                    return value === label || value.includes(label);
                }});
            }}

            function movePreview(event) {{
                const preview = ensurePreview();
                const margin = 18;
                const width = 166;
                const height = 250;
                let left = event.clientX + margin;
                let top = event.clientY + margin;

                if (left + width > parentWindow.innerWidth) {{
                    left = event.clientX - width - margin;
                }}

                if (top + height > parentWindow.innerHeight) {{
                    top = parentWindow.innerHeight - height - margin;
                }}

                preview.style.left = Math.max(12, left) + "px";
                preview.style.top = Math.max(12, top) + "px";
            }}

            function showPreview(option, event) {{
                const label = findLabel(option.textContent);
                const data = parentWindow.__cinescopePosterPreviewData || {{}};
                const movie = label ? data[label] : null;

                if (!movie || !movie.poster_url) {{
                    hidePreview();
                    return;
                }}

                const preview = ensurePreview();
                preview.innerHTML = `
                    <img
                        src="${{movie.poster_url}}"
                        alt="${{movie.title}} 포스터"
                        style="width:100%; border-radius:6px; display:block; margin-bottom:7px;"
                    >
                    <div style="font-weight:700; line-height:1.35;">${{label}}</div>
                `;
                preview.style.display = "block";
                movePreview(event);
            }}

            function hidePreview() {{
                const preview = ensurePreview();
                preview.style.display = "none";
            }}

            function hidePreviewIfOpen() {{
                const preview = parentDocument.getElementById("cinescope-selectbox-poster-preview");

                if (preview) {{
                    preview.style.display = "none";
                }}
            }}

            function bindOptions() {{
                const options = parentDocument.querySelectorAll('[role="option"]');

                options.forEach(function(option) {{
                    if (option.dataset.cinescopePosterHoverBound === "true") {{
                        return;
                    }}

                    option.dataset.cinescopePosterHoverBound = "true";
                    option.addEventListener("mouseenter", function(event) {{
                        showPreview(option, event);
                    }});
                    option.addEventListener("mousemove", function(event) {{
                        showPreview(option, event);
                    }});
                    option.addEventListener("mouseleave", hidePreview);
                    option.addEventListener("mousedown", hidePreviewIfOpen);
                    option.addEventListener("pointerdown", hidePreviewIfOpen);
                    option.addEventListener("click", hidePreviewIfOpen);
                }});
            }}

            function bindGlobalPreviewDismiss() {{
                if (parentWindow.__cinescopePosterPreviewDismissInstalled) {{
                    return;
                }}

                parentDocument.addEventListener("click", hidePreviewIfOpen, true);
                parentDocument.addEventListener("pointerdown", hidePreviewIfOpen, true);
                parentDocument.addEventListener("keydown", function(event) {{
                    if (event.key === "Escape" || event.key === "Enter") {{
                        hidePreviewIfOpen();
                    }}
                }}, true);
                parentWindow.addEventListener("scroll", hidePreviewIfOpen, true);
                parentWindow.addEventListener("blur", hidePreviewIfOpen);
                parentWindow.__cinescopePosterPreviewDismissInstalled = true;
            }}

            bindOptions();
            bindGlobalPreviewDismiss();

            if (!parentWindow.__cinescopePosterPreviewObserverInstalled) {{
                const observer = new MutationObserver(bindOptions);
                observer.observe(parentDocument.body, {{
                    childList: true,
                    subtree: true
                }});
                parentWindow.__cinescopePosterPreviewObserverInstalled = true;
            }}
        }})();
        </script>
        """,
        height=0,
        width=0
    )


def korean_date_select(
    label: str,
    value: date,
    key_prefix: str,
    min_year: int = 2000,
    max_year: int | None = None
):
    if max_year is None:
        max_year = date.today().year

    st.write(label)

    year_options = list(range(max_year, min_year - 1, -1))
    month_options = list(range(1, 13))

    col_year, col_month, col_day = st.columns(3)

    with col_year:
        selected_year = st.selectbox(
            "연도",
            year_options,
            index=year_options.index(value.year)
            if value.year in year_options else 0,
            key=f"{key_prefix}_year"
        )

    with col_month:
        selected_month = st.selectbox(
            "월",
            month_options,
            index=value.month - 1,
            format_func=lambda month: f"{month}월",
            key=f"{key_prefix}_month"
        )

    max_day = calendar.monthrange(selected_year, selected_month)[1]
    day_options = list(range(1, max_day + 1))
    selected_day_value = min(value.day, max_day)

    with col_day:
        selected_day = st.selectbox(
            "일",
            day_options,
            index=selected_day_value - 1,
            format_func=lambda day: f"{day}일",
            key=f"{key_prefix}_day"
        )

    return date(selected_year, selected_month, selected_day)


@st.dialog("영화 등록 완료")
def movie_created_dialog():
    created_movie = st.session_state.get("movie_create_success")

    st.success("영화 등록이 완료되었습니다.")
    st.caption("3초 후 자동으로 닫힙니다.")

    if created_movie:
        st.write(f"영화 제목: {created_movie['title']}")
        st.write(f"개봉일: {created_movie['release_date']}")
        st.write(f"감독: {created_movie['director']}")
        st.write(f"장르: {created_movie['genre']}")

    if st.button("바로 닫기", use_container_width=True, type="primary"):
        if "movie_create_success" in st.session_state:
            del st.session_state.movie_create_success
        st.rerun()

    time.sleep(3)

    if "movie_create_success" in st.session_state:
        del st.session_state.movie_create_success

    st.rerun()


@st.dialog("영화 수정 완료")
def movie_updated_dialog():
    updated_movie = st.session_state.get("movie_update_success")

    st.success("영화 정보 수정이 완료되었습니다.")
    st.caption("3초 후 자동으로 닫힙니다.")

    if updated_movie:
        st.write(f"영화 제목: {updated_movie['title']}")
        st.write(f"개봉일: {updated_movie['release_date']}")
        st.write(f"감독: {updated_movie['director']}")
        st.write(f"장르: {updated_movie['genre']}")

    if st.button("바로 닫기", use_container_width=True, type="primary"):
        if "movie_update_success" in st.session_state:
            del st.session_state.movie_update_success
        st.rerun()

    time.sleep(3)

    if "movie_update_success" in st.session_state:
        del st.session_state.movie_update_success

    st.rerun()


@st.dialog("영화 삭제 확인")
def movie_delete_confirm_dialog():
    target = st.session_state.get("movie_delete_target")

    if not target:
        st.warning("삭제할 영화 정보가 없습니다.")
        return

    st.error("정말 이 영화를 삭제하시겠습니까?")
    st.caption("연결된 리뷰도 함께 삭제됩니다.")

    st.write(f"영화 ID: {target['id']}")
    st.write(f"영화 제목: {target['title']}")
    st.write(f"개봉일: {target['release_date']}")
    st.write(f"감독: {target['director']}")

    col_yes, col_no = st.columns(2)

    with col_yes:
        if st.button("삭제", use_container_width=True, type="primary"):
            result = request_delete(f"/movies/{target['id']}")

            if result:
                st.session_state.movie_delete_target = None
                st.session_state.movie_action_message = result["message"]
                st.session_state.pending_page = "영화 목록"
                st.rerun()

    with col_no:
        if st.button("취소", use_container_width=True):
            st.session_state.movie_delete_target = None
            st.rerun()


@st.dialog("리뷰 등록 완료")
def review_created_dialog():
    last_review = st.session_state.get("last_created_review")

    st.success("리뷰 등록이 완료되었습니다.")

    if last_review:
        st.write(f"영화 제목: {last_review.get('movie_title', '제목 없음')}")
        st.write(f"작성자: {last_review['author']}")
        st.write(f"사용자 평점: {format_user_rating(last_review.get('user_rating'))}")
        st.write(f"리뷰 내용: {last_review['content']}")
        st.write(
            f"감성 분석 결과: {render_sentiment_badge(last_review['sentiment_label'])}"
        )
        st.write(f"감성 점수: {last_review['sentiment_score']}")

    col_add, col_recent = st.columns(2)

    with col_add:
        if st.button("리뷰 추가 등록하기", use_container_width=True):
            st.session_state.review_success_dialog_open = False
            st.session_state.show_recent_reviews_after_create = False

            if last_review and last_review.get("movie_id") is not None:
                st.session_state.review_create_selected_movie_id = last_review["movie_id"]

            # 입력 폼을 새로 만들기 위한 key 번호 증가
            st.session_state.review_form_reset_count = (
                st.session_state.get("review_form_reset_count", 0) + 1
            )

            if "last_created_review" in st.session_state:
                del st.session_state.last_created_review

            st.rerun()

    with col_recent:
        if st.button("최근 리뷰 보기", use_container_width=True):
            st.session_state.review_success_dialog_open = False
            st.session_state.show_recent_reviews_after_create = True
            st.session_state.review_offset = 0
            st.rerun()

@st.dialog("리뷰 수정 확인")
def review_update_confirm_dialog():
    target = st.session_state.get("review_update_target")

    if not target:
        st.warning("수정할 리뷰 정보가 없습니다.")
        return

    st.warning("정말 이 리뷰를 수정하시겠습니까?")

    st.write(f"리뷰 ID: {target['id']}")
    st.write(f"영화 제목: {target.get('movie_title', '제목 없음')}")
    st.write(f"수정 작성자: {target['author']}")
    st.write(f"수정 리뷰 내용: {target['content']}")
    st.write(f"수정 평점: {format_user_rating(target['user_rating'])}")

    col_yes, col_no = st.columns(2)

    with col_yes:
        if st.button("Yes", use_container_width=True, type="primary"):
            payload = {
                "author": target["author"],
                "content": target["content"],
                "user_rating": target["user_rating"]
            }

            result = request_patch(
                f"/reviews/{target['id']}",
                payload
            )

            if result:
                st.session_state.review_update_target = None
                st.session_state.editing_review_id = None
                st.session_state.review_action_message = "리뷰가 수정되었습니다."
                st.rerun()

    with col_no:
        if st.button("No", use_container_width=True):
            st.session_state.review_update_target = None
            st.rerun()


@st.dialog("리뷰 삭제 확인")
def review_delete_confirm_dialog():
    target = st.session_state.get("review_delete_target")

    if not target:
        st.warning("삭제할 리뷰 정보가 없습니다.")
        return

    st.error("정말 이 리뷰를 삭제하시겠습니까?")

    st.write(f"리뷰 ID: {target['id']}")
    st.write(f"영화 제목: {target.get('movie_title', '제목 없음')}")
    st.write(f"작성자: {target['author']}")
    st.write(f"리뷰 내용: {target['content']}")

    col_yes, col_no = st.columns(2)

    with col_yes:
        if st.button("Yes", use_container_width=True, type="primary"):
            result = request_delete(f"/reviews/{target['id']}")

            if result:
                st.session_state.review_delete_target = None
                st.session_state.review_action_message = "리뷰가 삭제되었습니다."
                st.rerun()

    with col_no:
        if st.button("No", use_container_width=True):
            st.session_state.review_delete_target = None
            st.rerun()

health = request_get("/")
if not health:
    st.warning("백엔드 서버 연결을 확인하십시오.")

if st.query_params.get("home") == "1":
    st.session_state.page_radio = "영화 목록"
    st.query_params.clear()

st.markdown(
    """
    <div class="cinescope-hero">
        <div class="cinescope-hero-main">
            <a class="cinescope-home-link" href="?home=1" target="_self" aria-label="홈으로 이동">
                <div class="cinescope-kicker">Movie Review Intelligence</div>
                <div class="cinescope-title">CineScope</div>
            </a>
            <div class="cinescope-copy">
                영화 포스터와 리뷰를 한 화면에서 살펴보고, 사용자 평점과 감성 분석 결과로
                작품별 반응을 빠르게 확인하는 영화 리뷰 분석 서비스입니다.
            </div>
        </div>
        <div class="cinescope-panel">
            <div>
                <div class="cinescope-panel-title">리뷰 기반 영화 분석</div>
                <div class="cinescope-panel-copy">
                    등록된 리뷰의 평점과 감성 결과를 모아 영화별 반응을 비교합니다.
                    포스터 중심의 카드 화면에서 주요 영화를 먼저 확인할 수 있습니다.
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

col_primary_action, col_secondary_action, _ = st.columns([1, 1, 3])

with col_primary_action:
    if st.button("리뷰 작성하기", use_container_width=True, type="primary"):
        navigate_to("리뷰 등록")

with col_secondary_action:
    if st.button("영화 등록하기", use_container_width=True):
        navigate_to("영화 등록")


PAGE_OPTIONS = [
    "영화 목록",
    "영화 등록",
    "영화 수정",
    "리뷰 등록",
    "영화별 리뷰",
    "통계 대시보드",
    "최근 리뷰"
]

if "page_radio" not in st.session_state:
    st.session_state.page_radio = "영화 목록"

if st.session_state.get("pending_page"):
    st.session_state.page_radio = st.session_state.pending_page
    del st.session_state.pending_page

if st.session_state.page_radio not in PAGE_OPTIONS:
    st.session_state.page_radio = "영화 목록"

active_page = st.session_state.page_radio

nav_columns = st.columns([0.5, 1, 1, 1, 1, 1, 1, 1, 0.5])

for index, page_name in enumerate(PAGE_OPTIONS, start=1):
    with nav_columns[index]:
        if st.button(
            page_name,
            key=f"nav_page_{index}",
            use_container_width=True,
            type="primary" if active_page == page_name else "secondary"
        ):
            st.session_state.page_radio = page_name
            st.rerun()


if active_page == "영화 목록":
    if st.session_state.get("movie_create_success"):
        movie_created_dialog()

    if st.session_state.get("movie_update_success"):
        movie_updated_dialog()

    if st.session_state.get("movie_action_message"):
        st.success(st.session_state.movie_action_message)
        del st.session_state.movie_action_message

    movies = get_movies()

    if not movies:
        st.info("등록된 영화가 없습니다. 먼저 영화를 등록하십시오.")
    else:
        st.markdown(
            """
            <div class="section-heading">
                <div>
                    <h2>추천 영화 3</h2>
                    <p>리뷰 반응, 평점, 최근 등록 기준으로 한 편씩 보여줍니다.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        featured_movies = get_featured_movies(movies)
        featured_columns = st.columns(3)

        for index, card in enumerate(featured_movies):
            with featured_columns[index]:
                render_movie_card(card, index)

        st.divider()

        with st.expander("전체 등록 영화 관리"):
            for movie in movies:
                rating = get_movie_rating(movie["id"])

                with st.container(border=True):
                    col_poster, col_info, col_action = st.columns([1, 3, 1])

                    with col_poster:
                        render_poster_image(movie.get("poster_url"), use_info=False)

                    with col_info:
                        st.markdown(f"### {movie['title']}")
                        st.write(f"개봉일: {movie['release_date']}")
                        st.write(f"감독: {movie['director']}")
                        st.write(f"장르: {movie['genre']}")

                        if rating:
                            if rating["average_rating_5"] is None:
                                st.write("평균 평점: 리뷰 없음")
                            else:
                                st.write(
                                    f"평균 평점: {format_user_rating(rating['average_rating_5'])}"
                                )
                                st.write(
                                    f"감성 요약: {render_sentiment_badge(rating['label_summary'])}"
                                )
                                st.write(f"리뷰 수: {rating['review_count']}개")

                    with col_action:
                        if st.button(
                            "삭제",
                            key=f"delete_movie_{movie['id']}",
                            type="secondary"
                        ):
                            result = request_delete(f"/movies/{movie['id']}")
                            if result:
                                st.success(result["message"])
                                st.rerun()


if active_page == "영화 등록":
    st.subheader("영화 등록")

    with st.form("movie_create_form"):
        title = st.text_input("영화 제목")
        release_date = korean_date_select(
            "개봉일",
            value=date.today(),
            key_prefix="movie_create_release_date"
        )
        director = st.text_input("감독")
        genre = st.text_input("장르")
        poster_url = st.text_input("포스터 URL")

        submitted = st.form_submit_button("영화 등록")

        if submitted:
            if not title or not director or not genre or not poster_url:
                st.warning("모든 항목을 입력하십시오.")
            else:
                existing_movies = get_movies()
                is_duplicate = any(
                    movie["title"].strip().lower() == title.strip().lower()
                    for movie in existing_movies
                )

                if is_duplicate:
                    st.warning("같은 제목의 영화가 이미 등록되어 있습니다.")
                    st.stop()

                payload = {
                    "title": title.strip(),
                    "release_date": release_date.isoformat(),
                    "director": director.strip(),
                    "genre": genre.strip(),
                    "poster_url": poster_url.strip()
                }

                result = request_post("/movies", payload)

                if result:
                    st.session_state.movie_create_success = result
                    st.session_state.pending_page = "영화 목록"
                    st.rerun()

if active_page == "영화 수정":
    st.subheader("영화 정보 수정")

    if st.session_state.get("movie_delete_target"):
        movie_delete_confirm_dialog()

    movies = get_movies()

    if not movies:
        st.info("수정할 영화가 없습니다.")
    else:
        inject_selectbox_poster_hover(movies)

        movie_options = {
            movie_option_label(movie): movie
            for movie in movies
        }

        selected_movie_label = st.selectbox(
            "수정할 영화 선택",
            list(movie_options.keys())
        )

        selected_movie = movie_options[selected_movie_label]
        render_selected_movie_preview(selected_movie)

        current_release_date = datetime.strptime(
            selected_movie["release_date"],
            "%Y-%m-%d"
        ).date()

        with st.form("movie_update_form"):
            title = st.text_input("영화 제목", value=selected_movie["title"])
            release_date = korean_date_select(
                "개봉일",
                value=current_release_date,
                key_prefix=f"movie_update_release_date_{selected_movie['id']}"
            )
            director = st.text_input("감독", value=selected_movie["director"])
            genre = st.text_input("장르", value=selected_movie["genre"])
            poster_url = st.text_input("포스터 URL", value=selected_movie["poster_url"])

            submitted = st.form_submit_button("영화 정보 수정")

            if submitted:
                if not title or not director or not genre or not poster_url:
                    st.warning("모든 항목을 입력하십시오.")
                else:
                    existing_movies = get_movies()
                    is_duplicate = any(
                        movie["id"] != selected_movie["id"]
                        and movie["title"].strip().lower() == title.strip().lower()
                        for movie in existing_movies
                    )

                    if is_duplicate:
                        st.warning("같은 제목의 영화가 이미 등록되어 있습니다.")
                        st.stop()

                    payload = {
                        "title": title.strip(),
                        "release_date": release_date.isoformat(),
                        "director": director.strip(),
                        "genre": genre.strip(),
                        "poster_url": poster_url.strip()
                    }

                    result = request_patch(
                        f"/movies/{selected_movie['id']}",
                        payload
                    )

                    if result:
                        st.session_state.movie_update_success = result
                        st.session_state.pending_page = "영화 목록"
                        st.rerun()

        st.divider()

        if st.button(
            "등록된 영화 삭제",
            key=f"movie_update_delete_{selected_movie['id']}",
            use_container_width=True,
            type="secondary"
        ):
            st.session_state.movie_delete_target = selected_movie
            st.rerun()

if active_page == "리뷰 등록":
    st.subheader("리뷰 등록")

    if "review_success_dialog_open" not in st.session_state:
        st.session_state.review_success_dialog_open = False

    if "show_recent_reviews_after_create" not in st.session_state:
        st.session_state.show_recent_reviews_after_create = False

    if "review_form_reset_count" not in st.session_state:
        st.session_state.review_form_reset_count = 0

    if st.session_state.review_success_dialog_open:
        review_created_dialog()

    movies = get_movies()

    if not movies:
        st.info("리뷰를 등록하려면 먼저 영화를 등록해야 합니다.")
    else:
        inject_selectbox_poster_hover(movies)

        movie_options = {
            movie_option_label(movie): movie
            for movie in movies
        }

        reset_key = st.session_state.review_form_reset_count
        requested_movie_id = st.session_state.get("review_create_selected_movie_id")
        review_movie_labels = list(movie_options.keys())
        review_movie_index = 0

        if requested_movie_id is not None:
            for option_index, option_label in enumerate(review_movie_labels):
                if movie_options[option_label]["id"] == requested_movie_id:
                    review_movie_index = option_index
                    break

            del st.session_state.review_create_selected_movie_id

        selected_movie_label = st.selectbox(
            "영화 선택",
            review_movie_labels,
            index=review_movie_index,
            key=f"review_movie_select_{reset_key}"
        )
        selected_movie = movie_options[selected_movie_label]
        render_selected_movie_preview(selected_movie)

        with st.form(f"review_create_form_{reset_key}"):
            author = st.text_input(
                "작성자",
                key=f"review_author_{reset_key}"
            )

            user_rating = st.slider(
                "사용자 평점",
                min_value=1.0,
                max_value=5.0,
                value=4.0,
                step=0.5,
                key=f"review_user_rating_{reset_key}"
            )

            content = st.text_area(
                "리뷰 내용",
                height=150,
                key=f"review_content_{reset_key}"
            )

            submitted = st.form_submit_button("리뷰 등록")

            if submitted:
                if not author or not content:
                    st.warning("작성자와 리뷰 내용을 입력하십시오.")
                else:
                    selected_movie_id = selected_movie["id"]

                    payload = {
                        "movie_id": selected_movie_id,
                        "author": author,
                        "content": content,
                        "user_rating": user_rating
                    }

                    result = request_post("/reviews", payload)

                    if result:
                        st.session_state.last_created_review = result
                        st.session_state.review_offset = 0
                        st.session_state.review_success_dialog_open = True
                        st.session_state.show_recent_reviews_after_create = False
                        st.rerun()

    if st.session_state.show_recent_reviews_after_create:
        st.divider()
        st.subheader("최근 리뷰 목록")

        review_data = get_reviews_page(limit=10, offset=0)
        reviews = review_data["reviews"]

        if not reviews:
            st.info("등록된 리뷰가 없습니다.")
        else:
            st.write(f"최근 리뷰 {len(reviews)}개를 표시합니다.")

            for review in reviews:
                with st.container(border=True):
                    st.write(f"리뷰 ID: {review['id']}")
                    st.write(f"영화 제목: {review.get('movie_title', '제목 없음')}")
                    st.write(f"영화 ID: {review['movie_id']}")
                    st.write(f"작성자: {review['author']}")
                    st.write(f"사용자 평점: {format_user_rating(review.get('user_rating'))}")
                    st.write(f"등록일: {review['created_at']}")
                    st.write(f"리뷰 내용: {review['content']}")
                    st.write(
                        f"감성 분석 결과: {render_sentiment_badge(review['sentiment_label'])}"
                    )
                    st.write(f"감성 점수: {review['sentiment_score']}")

            if st.button("최근 리뷰 접기"):
                st.session_state.show_recent_reviews_after_create = False
                st.rerun()

if active_page == "영화별 리뷰":
    st.subheader("영화별 리뷰 보기")

    if "editing_review_id" not in st.session_state:
        st.session_state.editing_review_id = None

    if st.session_state.get("review_update_target"):
        review_update_confirm_dialog()

    if st.session_state.get("review_delete_target"):
        review_delete_confirm_dialog()

    if st.session_state.get("review_action_message"):
        st.success(st.session_state.review_action_message)
        del st.session_state.review_action_message

    movies = get_movies()

    if not movies:
        st.info("등록된 영화가 없습니다.")
    else:
        inject_selectbox_poster_hover(movies)

        movie_options = {
            movie_option_label(movie): movie
            for movie in movies
        }
        movie_review_labels = list(movie_options.keys())
        requested_movie_id = st.session_state.get("movie_reviews_selected_id")
        movie_review_index = 0

        if requested_movie_id is not None:
            for option_index, option_label in enumerate(movie_review_labels):
                if movie_options[option_label]["id"] == requested_movie_id:
                    movie_review_index = option_index
                    break

            del st.session_state.movie_reviews_selected_id

        selected_movie_label = st.selectbox(
            "리뷰를 확인할 영화 선택",
            movie_review_labels,
            index=movie_review_index,
            key="movie_reviews_select"
        )

        selected_movie = movie_options[selected_movie_label]
        selected_movie_id = selected_movie["id"]

        reviews = get_reviews_by_movie(selected_movie_id)

        col_poster, col_info = st.columns([1, 3])

        with col_poster:
            render_poster_image(selected_movie.get("poster_url"), use_info=False)

        with col_info:
            st.markdown(f"## {selected_movie['title']}")
            st.write(f"개봉일: {selected_movie['release_date']}")
            st.write(f"감독: {selected_movie['director']}")
            st.write(f"장르: {selected_movie['genre']}")

        st.divider()

        review_count = len(reviews)

        user_ratings = [
            review.get("user_rating")
            for review in reviews
            if review.get("user_rating") is not None
        ]

        sentiment_scores = [
            review.get("sentiment_score")
            for review in reviews
            if review.get("sentiment_score") is not None
        ]

        positive_count = sum(
            1 for review in reviews
            if review.get("sentiment_label") == "positive"
        )

        neutral_count = sum(
            1 for review in reviews
            if review.get("sentiment_label") == "neutral"
        )

        negative_count = sum(
            1 for review in reviews
            if review.get("sentiment_label") == "negative"
        )

        average_user_rating = (
            sum(user_ratings) / len(user_ratings)
            if user_ratings
            else None
        )

        average_sentiment_score = (
            sum(sentiment_scores) / len(sentiment_scores)
            if sentiment_scores
            else None
        )

        col_count, col_user_avg, col_ai_avg, col_sentiment = st.columns(4)

        with col_count:
            st.metric("리뷰 수", f"{review_count}개")

        with col_user_avg:
            st.metric(
                "사용자 평균 평점",
                format_user_rating(average_user_rating)
            )

        with col_ai_avg:
            st.metric(
                "AI 평균 감성 점수",
                format_sentiment_score(average_sentiment_score)
            )

        with col_sentiment:
            st.write("감성 분포")
            st.write(f"긍정: {positive_count}개")
            st.write(f"중립: {neutral_count}개")
            st.write(f"부정: {negative_count}개")

        st.divider()

        if not reviews:
            st.info("이 영화에 등록된 리뷰가 없습니다.")
        else:
            st.markdown("### 등록된 리뷰")

            for review in reviews:
                with st.container(border=True):
                    col_main, col_score = st.columns([4, 1])

                    with col_main:
                        st.caption(f"리뷰 ID {review['id']} · 영화 ID {review['movie_id']}")

                        st.markdown("**작성자**")
                        st.write(review["author"])

                        st.markdown("**리뷰 내용**")
                        st.write(review["content"])

                    with col_score:
                        st.metric(
                            "사용자 평점",
                            format_user_rating(review.get("user_rating"))
                        )

                        st.metric(
                            "AI 감성 점수",
                            format_sentiment_score(review.get("sentiment_score"))
                        )

                        st.write(
                            f"감성 결과: **{render_sentiment_badge(review.get('sentiment_label'))}**"
                        )

                    st.divider()

                    col_date, col_edit, col_delete = st.columns([3, 1, 1])

                    with col_date:
                        st.caption(f"등록일: {review['created_at']}")

                    with col_edit:
                        if st.button(
                            "리뷰 수정",
                            key=f"movie_reviews_open_edit_{review['id']}",
                            use_container_width=True
                        ):
                            if st.session_state.editing_review_id == review["id"]:
                                st.session_state.editing_review_id = None
                            else:
                                st.session_state.editing_review_id = review["id"]

                            st.rerun()

                    with col_delete:
                        if st.button(
                            "리뷰 삭제",
                            key=f"movie_reviews_delete_{review['id']}",
                            use_container_width=True,
                            type="secondary"
                        ):
                            st.session_state.review_delete_target = review
                            st.rerun()

                    if st.session_state.editing_review_id == review["id"]:
                        st.divider()
                        st.markdown("#### 리뷰 수정")

                        with st.form(f"movie_reviews_update_form_{review['id']}"):
                            edit_author = st.text_input(
                                "작성자 수정",
                                value=review["author"],
                                key=f"movie_reviews_edit_author_{review['id']}"
                            )

                            edit_user_rating = st.slider(
                                "사용자 평점 수정",
                                min_value=1.0,
                                max_value=5.0,
                                value=float(review.get("user_rating") or 4.0),
                                step=0.5,
                                key=f"movie_reviews_edit_user_rating_{review['id']}"
                            )

                            edit_content = st.text_area(
                                "리뷰 내용 수정",
                                value=review["content"],
                                height=120,
                                key=f"movie_reviews_edit_content_{review['id']}"
                            )

                            col_save, col_cancel = st.columns(2)

                            with col_save:
                                update_submitted = st.form_submit_button(
                                    "리뷰 수정 저장",
                                    use_container_width=True
                                )

                            with col_cancel:
                                cancel_submitted = st.form_submit_button(
                                    "수정 취소",
                                    use_container_width=True
                                )

                            if update_submitted:
                                if not edit_author or not edit_content:
                                    st.warning("작성자와 리뷰 내용을 모두 입력하십시오.")
                                else:
                                    st.session_state.review_update_target = {
                                        "id": review["id"],
                                        "movie_title": review.get(
                                            "movie_title",
                                            selected_movie["title"]
                                        ),
                                        "author": edit_author,
                                        "content": edit_content,
                                        "user_rating": edit_user_rating
                                    }
                                    st.rerun()

                            if cancel_submitted:
                                st.session_state.editing_review_id = None
                                st.rerun()

if active_page == "통계 대시보드":
    st.subheader("통계 대시보드")

    movies = get_movies()
    reviews = get_all_reviews()

    total_movie_count = len(movies)
    total_review_count = len(reviews)

    user_rating_values = [
        review.get("user_rating")
        for review in reviews
        if review.get("user_rating") is not None
    ]

    sentiment_score_values = [
        review.get("sentiment_score")
        for review in reviews
        if review.get("sentiment_score") is not None
    ]

    average_user_rating = safe_average(user_rating_values)
    average_sentiment_score = safe_average(sentiment_score_values)

    positive_count = sum(
        1 for review in reviews
        if review.get("sentiment_label") == "positive"
    )

    neutral_count = sum(
        1 for review in reviews
        if review.get("sentiment_label") == "neutral"
    )

    negative_count = sum(
        1 for review in reviews
        if review.get("sentiment_label") == "negative"
    )

    st.markdown("### 전체 요약")

    col_movie, col_review, col_user_rating, col_ai_score = st.columns(4)

    with col_movie:
        st.metric("전체 영화 수", f"{total_movie_count}개")

    with col_review:
        st.metric("전체 리뷰 수", f"{total_review_count}개")

    with col_user_rating:
        st.metric(
            "전체 사용자 평균 평점",
            format_user_rating(average_user_rating)
        )

    with col_ai_score:
        st.metric(
            "전체 AI 평균 감성 점수",
            format_sentiment_score(average_sentiment_score)
        )

    st.divider()

    st.markdown("### 감성 분석 분포")

    col_positive, col_neutral, col_negative = st.columns(3)

    with col_positive:
        st.metric("긍정 리뷰", f"{positive_count}개")

    with col_neutral:
        st.metric("중립 리뷰", f"{neutral_count}개")

    with col_negative:
        st.metric("부정 리뷰", f"{negative_count}개")

    if total_review_count > 0:
        st.write("감성 비율")

        positive_ratio = positive_count / total_review_count
        neutral_ratio = neutral_count / total_review_count
        negative_ratio = negative_count / total_review_count

        st.write(f"긍정: {positive_ratio:.1%}")
        st.progress(positive_ratio)

        st.write(f"중립: {neutral_ratio:.1%}")
        st.progress(neutral_ratio)

        st.write(f"부정: {negative_ratio:.1%}")
        st.progress(negative_ratio)

    st.divider()

    st.markdown("### 영화별 통계")

    movie_stats = []

    for movie in movies:
        movie_reviews = [
            review for review in reviews
            if review.get("movie_id") == movie["id"]
        ]

        movie_user_ratings = [
            review.get("user_rating")
            for review in movie_reviews
            if review.get("user_rating") is not None
        ]

        movie_sentiment_scores = [
            review.get("sentiment_score")
            for review in movie_reviews
            if review.get("sentiment_score") is not None
        ]

        movie_positive_count = sum(
            1 for review in movie_reviews
            if review.get("sentiment_label") == "positive"
        )

        movie_neutral_count = sum(
            1 for review in movie_reviews
            if review.get("sentiment_label") == "neutral"
        )

        movie_negative_count = sum(
            1 for review in movie_reviews
            if review.get("sentiment_label") == "negative"
        )

        movie_average_user_rating = safe_average(movie_user_ratings)
        movie_average_sentiment_score = safe_average(movie_sentiment_scores)

        movie_stats.append(
            {
                "영화 제목": movie["title"],
                "리뷰 수": len(movie_reviews),
                "사용자 평균 평점": format_user_rating(movie_average_user_rating),
                "AI 평균 감성 점수": format_sentiment_score(movie_average_sentiment_score),
                "긍정": movie_positive_count,
                "중립": movie_neutral_count,
                "부정": movie_negative_count
            }
        )

    if not movie_stats:
        st.info("표시할 영화 통계가 없습니다.")
    else:
        st.table(movie_stats)

    st.divider()

    condition_rows = []

    for movie in movies:
        movie_review_count = sum(
            1 for review in reviews
            if review.get("movie_id") == movie["id"]
        )


if active_page == "최근 리뷰":
    st.subheader("리뷰 목록")

    # 수정 중인 리뷰 ID 관리
    if "editing_review_id" not in st.session_state:
        st.session_state.editing_review_id = None

    # 리뷰 수정 확인 팝업
    if st.session_state.get("review_update_target"):
        review_update_confirm_dialog()

    # 리뷰 삭제 확인 팝업
    if st.session_state.get("review_delete_target"):
        review_delete_confirm_dialog()

    # 수정/삭제 완료 메시지
    if st.session_state.get("review_action_message"):
        st.success(st.session_state.review_action_message)
        del st.session_state.review_action_message

    # 페이지 상태 초기화
    if "review_offset" not in st.session_state:
        st.session_state.review_offset = 0

    if "review_limit" not in st.session_state:
        st.session_state.review_limit = 10

    selected_limit = st.radio(
        "페이지당 표시 개수",
        [10, 20],
        horizontal=True,
        index=0 if st.session_state.review_limit == 10 else 1
    )

    if selected_limit != st.session_state.review_limit:
        st.session_state.review_limit = selected_limit
        st.session_state.review_offset = 0
        st.session_state.editing_review_id = None
        st.rerun()

    review_data = get_reviews_page(
        limit=st.session_state.review_limit,
        offset=st.session_state.review_offset
    )

    total_count = review_data["total_count"]
    reviews = review_data["reviews"]

    start_no = st.session_state.review_offset + 1 if total_count > 0 else 0
    end_no = st.session_state.review_offset + len(reviews)

    st.write(f"표시 범위: {start_no} ~ {end_no} / 총 {total_count}개")

    if not reviews:
        st.info("등록된 리뷰가 없습니다.")
    else:
        for review in reviews:
            with st.container(border=True):
                col_main, col_side = st.columns([4, 1])

                with col_main:
                    st.markdown(f"### {review.get('movie_title', '제목 없음')}")
                    st.caption(f"리뷰 ID {review['id']} · 영화 ID {review['movie_id']}")

                    st.markdown("**작성자**")
                    st.write(review["author"])

                    st.markdown("**리뷰 내용**")
                    st.write(review["content"])

                with col_side:
                    st.metric(
                        label="사용자 평점",
                        value=format_user_rating(review.get("user_rating"))
                    )

                    st.metric(
                        label="AI 감성 점수",
                        value=format_sentiment_score(review.get("sentiment_score"))
                    )

                    st.write(
                        f"감성 결과: **{render_sentiment_badge(review.get('sentiment_label'))}**"
                    )

                st.divider()

                col_date, col_edit, col_delete = st.columns([3, 1, 1])

                with col_date:
                    st.caption(f"등록일: {review['created_at']}")

                with col_edit:
                    if st.button(
                        "리뷰 수정",
                        key=f"open_edit_review_{review['id']}",
                        use_container_width=True
                    ):
                        if st.session_state.editing_review_id == review["id"]:
                            st.session_state.editing_review_id = None
                        else:
                            st.session_state.editing_review_id = review["id"]

                        st.rerun()

                with col_delete:
                    if st.button(
                        "리뷰 삭제",
                        key=f"delete_review_{review['id']}",
                        use_container_width=True,
                        type="secondary"
                    ):
                        st.session_state.review_delete_target = review
                        st.rerun()

                # 선택된 리뷰만 수정 폼 표시
                if st.session_state.editing_review_id == review["id"]:
                    st.divider()
                    st.markdown("#### 리뷰 수정")

                    with st.form(f"review_update_form_{review['id']}"):
                        edit_author = st.text_input(
                            "작성자 수정",
                            value=review["author"],
                            key=f"edit_author_{review['id']}"
                        )

                        edit_user_rating = st.slider(
                            "사용자 평점 수정",
                            min_value=1.0,
                            max_value=5.0,
                            value=float(review.get("user_rating") or 4.0),
                            step=0.5,
                            key=f"edit_user_rating_{review['id']}"
                        )

                        edit_content = st.text_area(
                            "리뷰 내용 수정",
                            value=review["content"],
                            height=120,
                            key=f"edit_content_{review['id']}"
                        )

                        col_save, col_cancel = st.columns(2)

                        with col_save:
                            update_submitted = st.form_submit_button(
                                "리뷰 수정 저장",
                                use_container_width=True
                            )

                        with col_cancel:
                            cancel_submitted = st.form_submit_button(
                                "수정 취소",
                                use_container_width=True
                            )

                        if update_submitted:
                            if not edit_author or not edit_content:
                                st.warning("작성자와 리뷰 내용을 모두 입력하십시오.")
                            else:
                                st.session_state.review_update_target = {
                                    "id": review["id"],
                                    "movie_title": review.get("movie_title", "제목 없음"),
                                    "author": edit_author,
                                    "content": edit_content,
                                    "user_rating": edit_user_rating
                                }
                                st.rerun()

                        if cancel_submitted:
                            st.session_state.editing_review_id = None
                            st.rerun()

    st.divider()

    col_prev, col_page, col_next = st.columns([1, 2, 1])

    with col_prev:
        if st.button(
            "이전 페이지",
            disabled=st.session_state.review_offset == 0,
            use_container_width=True
        ):
            st.session_state.review_offset = max(
                0,
                st.session_state.review_offset - st.session_state.review_limit
            )
            st.session_state.editing_review_id = None
            st.rerun()

    with col_page:
        current_page = (
            st.session_state.review_offset // st.session_state.review_limit
        ) + 1

        total_page = (
            (total_count - 1) // st.session_state.review_limit
        ) + 1 if total_count > 0 else 1

        st.write(f"현재 페이지: {current_page} / {total_page}")

    with col_next:
        has_next = (
            st.session_state.review_offset + st.session_state.review_limit
            < total_count
        )

        if st.button(
            "다음 페이지",
            disabled=not has_next,
            use_container_width=True
        ):
            st.session_state.review_offset += st.session_state.review_limit
            st.session_state.editing_review_id = None
            st.rerun()
