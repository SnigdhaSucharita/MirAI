import numpy as np
from typing import List
from collections import Counter, defaultdict

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from app.models.clip_model import encode_text


analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str) -> str:
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "positive"
    if score <= -0.05:
        return "negative"
    return "neutral"


def sentiment_distribution(sentiments: List[str]) -> dict:
    total = len(sentiments)
    counts = Counter(sentiments)
    return {
        k: round((v / total) * 100, 2)
        for k, v in counts.items()
    }


def cluster_reviews(reviews: List[str], k: int):
    embeddings = np.array([
    encode_text(r).reshape(-1)
    for r in reviews
    ])
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(embeddings)
    return labels


def extract_keywords(texts: List[str], top_k=3):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=20
    )
    tfidf = vectorizer.fit_transform(texts)
    scores = np.mean(tfidf.toarray(), axis=0)
    keywords = np.array(vectorizer.get_feature_names_out())
    top = keywords[np.argsort(scores)[-top_k:]]
    return top.tolist()


def build_review_insights(movie_id: int, reviews: List[str]):
    reviews = list(set(reviews))  # de-duplicate

    if len(reviews) < 2:
        return {
            "movie_id": movie_id,
            "sentiment_summary": {},
            "top_praises": [],
            "top_criticisms": [],
            "themes": []
        }

    sentiments = [analyze_sentiment(r) for r in reviews]
    sentiment_summary = sentiment_distribution(sentiments)

    k = min(4, len(reviews))
    labels = cluster_reviews(reviews, k)

    clusters = defaultdict(list)
    cluster_sentiments = defaultdict(list)

    for review, label, sentiment in zip(reviews, labels, sentiments):
        clusters[label].append(review)
        cluster_sentiments[label].append(sentiment)

    themes = []
    praises = []
    criticisms = []

    for label, texts in clusters.items():
        keywords = extract_keywords(texts)
        sentiment_counts = Counter(cluster_sentiments[label])

        if sentiment_counts["positive"] > sentiment_counts["negative"]:
            overall = "positive"
            praises.extend(keywords)
        elif sentiment_counts["negative"] > sentiment_counts["positive"]:
            overall = "negative"
            criticisms.extend(keywords)
        else:
            overall = "mixed"

        themes.append({
            "theme": " / ".join(keywords),
            "sentiment": overall,
            "examples": texts[:2]
        })

    return {
        "movie_id": movie_id,
        "sentiment_summary": sentiment_summary,
        "top_praises": list(set(praises))[:5],
        "top_criticisms": list(set(criticisms))[:5],
        "themes": themes
    }
