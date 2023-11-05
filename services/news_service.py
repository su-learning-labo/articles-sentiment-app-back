import requests
from sqlalchemy.orm import Session
from transformers import pipeline
from typing import List, Dict
from schemas import NewsArticleCreate, SentimentAnalysisCreate
from crud import crud_news

# NewsAPIの設定
NEWSAPI_URL = 'https://newsapi.org/v2/top-headlines'
API_KEY = '51d1ce9cbff14d41805389d2c5e62754'
HEADERS = {'X-Api-Key': API_KEY}

# 感情分析のためのモデルをロード
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
)


def fetch_news_articles():
    params = {
        'API_KEY': API_KEY,
        'country': 'jp',
        'language': 'jp',
        'pageSize': 100,
    }

    response = requests.get(url=NEWSAPI_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    articles = response.json()['articles']

    return articles


def analyze_sentiment(text: str) -> Dict:
    result = sentiment_analyzer(text)[0]
    return {
        'label': result['label'],
        'score': result['score'],
    }


def reanalyze_article_sentiment(db: Session, article_id: int):
    db_article = crud_news.get_news(db, news_id=article_id)
    if not db_article:
        return None

    new_sentiment_result = analyze_sentiment(db_article.description)

    updated_analysis = crud_news.update_sentiment_analysis(
        db=db,
        analysis_id=article_id,
        new_sentiment=new_sentiment_result['label'],
        new_score=new_sentiment_result['score'],
    )

    return updated_analysis


def save_news_and_sentiment(db: Session, article_data: dict, ranking: int):
    # ニュース記事を保存
    article_data = NewsArticleCreate(
        title=article_data['title'],
        description=article_data['description'],
        url=article_data['url'],
        published_at=article_data['publishedAt'],
        source_name=article_data['source']['name'],
        ranking=ranking,
    )
    db_article = crud_news.create_news_article(db=db, news=article_data)

    # 感情分析の実行
    sentiment_result = analyze_sentiment(article_data['description'])
    sentiment = SentimentAnalysisCreate(
        article_id=db_article.id,
        sentiment=sentiment_result['label'],
        score=sentiment_result['score']
    )
    crud_news.create_sentiment_analysis(db=db, analysis=sentiment)


def perform_and_save_sentiment_analysis(db: Session):
    all_news_articles = crud_news.get_all_news(db)

    for article in all_news_articles:
        sentiment_result = sentiment_analyzer(article.description)

        sentiment_data = SentimentAnalysisCreate(
            article_id = article.id,
            sentiment=sentiment_result[0]['label'],
            score=sentiment_result[0]['score']
        )
        crud_news.create_sentiment_analysis(db, sentiment_data)


def fetch_and_analyze_news(db: Session):
    params = {
        'API_KEY': API_KEY,
        'country': 'jp',
        'language': 'jp',
        'pageSize': 100,
    }

    response = requests.get(url=NEWSAPI_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    articles = response.json()['articles']

    for index, article in enumerate(articles):
        news_data = NewsArticleCreate(
            title=article['title'],
            description=article['description'],
            url=article['url'],
            published_at=article['publishedAt'],
            source_name=article['source']['name'],
            ranking=index + 1
        )
        db_article = crud_news.create_news_article(db, news_data)

        sentiment_result = sentiment_analyzer(article.get('description', '') or '')
        sentiment_data = SentimentAnalysisCreate(
            article_id=db_article.id,
            sentiment=sentiment_result[0]['label'],
            score=sentiment_result[0]['score']
        )
        crud_news.create_sentiment_analysis(db, sentiment_data)
