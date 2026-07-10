from functools import lru_cache

try:
    from transformers import pipeline
except Exception:
    pipeline = None


MODEL_NAME = "sangrimlee/bert-base-multilingual-cased-nsmc"
NEUTRAL_CONFIDENCE_THRESHOLD = 0.55


POSITIVE_WORDS = [
    "좋다", "좋고", "좋습니다", "좋았", "좋았습니다",
    "재미", "재밌", "재밌게", "감동", "추천",
    "몰입", "훌륭", "인상적", "최고", "만족",
    "완성도", "뛰어났", "잘 봤", "잘봤",
    "또 보고", "다시 보고", "2편", "후속", "제작해주세요",
    "행운", "보러가세요", "보러 가세요", "꼭 봐", "꼭 보",
    "명작", "수작", "강추", "한시간처럼", "시간처럼",
    "긴말 안", "긴 말 안"
]

NEGATIVE_WORDS = [
    "별로", "지루", "최악", "실망", "아쉽", "부족",
    "노잼", "산만", "불편", "아깝", "재미없",
    "못보겠", "못 보겠", "징그럽", "징그러", "불쾌",
    "싫다", "싫었", "별점 낮"
]


def analyze_sentiment_rule_based(text: str) -> dict:
    positive_count = sum(1 for word in POSITIVE_WORDS if word in text)
    negative_count = sum(1 for word in NEGATIVE_WORDS if word in text)

    if positive_count > negative_count:
        return {
            "label": "positive",
            "score": 0.9
        }

    if negative_count > positive_count:
        return {
            "label": "negative",
            "score": 0.1
        }

    return {
        "label": "neutral",
        "score": 0.5
    }


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    if pipeline is None:
        return None

    try:
        model = pipeline(
            task="sentiment-analysis",
            model=MODEL_NAME,
            tokenizer=MODEL_NAME
        )
        print("[INFO] Hugging Face sentiment model loaded")
        return model
    except Exception as error:
        print(f"[WARN] Hugging Face 모델 로딩 실패: {error}")
        return None


def normalize_model_result(result: dict) -> dict:
    raw_label = str(result.get("label", "")).lower()
    confidence = float(result.get("score", 0.0))

    if raw_label == "positive":
        return {
            "label": "positive",
            "score": round(confidence, 3)
        }

    if raw_label == "negative":
        return {
            "label": "negative",
            "score": round(1.0 - confidence, 3)
        }

    if raw_label in ["label_1", "1", "pos", "긍정"]:
        return {
            "label": "positive",
            "score": round(confidence, 3)
        }

    if raw_label in ["label_0", "0", "neg", "부정"]:
        return {
            "label": "negative",
            "score": round(1.0 - confidence, 3)
        }

    return {
        "label": "neutral",
        "score": 0.5
    }


def apply_review_domain_rule(text: str, model_result: dict) -> dict:
    positive_count = sum(1 for word in POSITIVE_WORDS if word in text)
    negative_count = sum(1 for word in NEGATIVE_WORDS if word in text)

    # 명확한 긍정 표현이 많은 경우
    if positive_count >= 2 and negative_count == 0:
        return {
            "label": "positive",
            "score": max(model_result["score"], 0.85)
        }

    # 명확한 부정 표현이 많은 경우
    if negative_count >= 2 and positive_count == 0:
        return {
            "label": "negative",
            "score": min(model_result["score"], 0.2)
        }

    # 긍정/부정 표현이 섞인 경우
    if positive_count >= 1 and negative_count >= 1:
        return {
            "label": "neutral",
            "score": 0.5
        }

    return model_result


def apply_user_rating_rule(model_result: dict, user_rating: float | None = None) -> dict:
    if user_rating is None:
        return model_result

    try:
        rating = float(user_rating)
    except (TypeError, ValueError):
        return model_result

    if rating >= 4.5:
        return {
            "label": "positive",
            "score": max(model_result["score"], 0.85)
        }

    if rating >= 4.0 and model_result["label"] == "negative":
        return {
            "label": "neutral",
            "score": 0.55
        }

    if rating <= 1.5:
        return {
            "label": "negative",
            "score": min(model_result["score"], 0.15)
        }

    if rating <= 2.0 and model_result["label"] == "positive":
        return {
            "label": "neutral",
            "score": 0.45
        }

    return model_result


def analyze_sentiment(text: str, user_rating: float | None = None) -> dict:
    if not text or not text.strip():
        return apply_user_rating_rule({
            "label": "neutral",
            "score": 0.5
        }, user_rating)

    sentiment_pipeline = get_sentiment_pipeline()

    if sentiment_pipeline is None:
        rule_result = analyze_sentiment_rule_based(text)
        return apply_user_rating_rule(rule_result, user_rating)

    try:
        result = sentiment_pipeline(text[:512])[0]
        model_result = normalize_model_result(result)
        domain_result = apply_review_domain_rule(text, model_result)
        return apply_user_rating_rule(domain_result, user_rating)
    except Exception as error:
        print(f"[WARN] Hugging Face 추론 실패: {error}")
        rule_result = analyze_sentiment_rule_based(text)
        return apply_user_rating_rule(rule_result, user_rating)
