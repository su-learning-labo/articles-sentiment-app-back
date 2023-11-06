from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from database import SessionLocal
from schemas import NewsArticleCreate, NewsArticle, SentimentAnalysisCreate, SentimentAnalysis, SentimentAnalysisUpdate
from services.news_service import fetch_news_articles, analyze_sentiment, reanalyze_article_sentiment, fetch_and_analyze_news, perform_and_save_sentiment_analysis
from crud import crud_news

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/articles/", response_model=List[NewsArticle])
# DBに保存されているニュース記事を呼び出す
def read_articles(db: Session = Depends(get_db)):
    articles = crud_news.get_all_news(db=db)
    return articles


@router.get('/sentiments/', response_model=List[SentimentAnalysis])
def read_sentiments(db: Session = Depends(get_db)):
    sentiments = crud_news.get_all_sentiments(db=db)
    return sentiments


@router.get("/articles/{article_id}", response_model=NewsArticle)
# 指定したIDの記事を呼び出す
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = crud_news.get_news(db=db, news_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article


@router.post('/articles/')
# NewsAPIから記事を取得し、DBに保存する
def create_article(db: Session = Depends(get_db)):
    articles = fetch_news_articles()

    for index, article in enumerate(articles, start=1):
        news = NewsArticleCreate(
            title=article['title'],
            description=article['description'],
            url=article['url'],
            published_at=article['publishedAt'],
            source_name=article['source']['name'],
            ranking=index
        )

        crud_news.create_news_article(db=db, news=news)

    return {'status': 'success', 'message': 'News fetched and saved successfully.'}


@router.post('/analyze-all-articles/')
def analyze_all_articles(db: Session = Depends(get_db)):
    perform_and_save_sentiment_analysis(db)
    return {'message': 'Sentiment analysis performed and saved for all articles.'}


@router.get('/articles/{article_id}/sentiment/', response_model=SentimentAnalysis)
# 指定した記事IDの感情分析結果を呼び出す
def read_sentiment(article_id: int, db: Session = Depends(get_db)):
    db_sentiment = crud_news.get_article_sentiment(db=db, article_id=article_id)
    if db_sentiment is None:
        raise HTTPException(status_code=404, detail='Article not found')
    return db_sentiment


@router.post("/articles/{article_id}/sentiment/")
# IDを指定してDBに保存してある記事を呼び出し、感情分析結果をDBに保存する
def analyze_article(article_id: int, db: Session = Depends(get_db)):
    db_article = crud_news.get_news(db, news_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail='Article not found')

    sentiment_result = analyze_sentiment(db_article.description)
    sentiment_data = SentimentAnalysisCreate(
        article_id=article_id,
        sentiment=sentiment_result['label'],
        score=sentiment_result['score'],
    )
    return crud_news.create_sentiment_analysis(db=db, analysis=sentiment_data)


@router.put('/articles/{article_id}/reanalyze_sentiment/', response_model=SentimentAnalysis)
# 記事を指定して、感情分析結果を更新する
def reanalyze_sentiment(article_id: int, db: Session = Depends(get_db)):
    updated_analysis = reanalyze_article_sentiment(db, article_id)

    if updated_analysis is None:
        raise HTTPException(status_code=404, detail='Article not found or sentiment analysis could not be updated')

    return updated_analysis


@router.post('/fetch-and-analyze/')
# 記事の取得〜感情分析までを一括で実施、DBに保存
def fetch_and_analyze(db: Session = Depends(get_db)):
    fetch_and_analyze_news(db=db)

    return {'message': 'Articles fetched, analyzed, and saved successfully.'}


if __name__ == "__main__":
    read_sentiment(article_id=3)
