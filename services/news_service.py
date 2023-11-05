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


def get_and_save_all_articles(db: Session):
    article_data = fetch_news_articles()
    for ranking, article_data in enumerate(article_data, start=1):
        save_news_and_sentiment(db=db, article_data=article_data, ranking=ranking)
