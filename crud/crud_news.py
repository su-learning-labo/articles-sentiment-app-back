from sqlalchemy.orm import Session
from datetime import datetime
from models import NewsArticle, SentimentAnalysis
from schemas import NewsArticleCreate, SentimentAnalysisCreate
# from services.news_service import analyze_sentiment


def get_all_news(db: Session):
    return db.query(NewsArticle).all()


def get_articles(db: Session, skip: int = 0, limit: int = 20):
    return db.query(NewsArticle).offset(skip).limit(limit).all()


def get_news(db: Session, news_id: int):
    return db.query(NewsArticle).filter(NewsArticle.id == news_id).first()


# def get_news_by_ranking(db: Session, ranking: int):
#     return db.query(NewsArticle).filter(NewsArticle.ranking == ranking).first()


def create_news_article(db: Session, news: NewsArticleCreate):
    db_news = NewsArticle(**news.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


def get_all_sentiments(db: Session):
    return db.query(SentimentAnalysis).all()


def get_sentiment_analysis(db: Session, analysis_id: int):
    return db.query(SentimentAnalysis).filter(SentimentAnalysis.id == analysis_id).first()


def get_article_sentiment(db: Session, article_id: int):
    return db.query(SentimentAnalysis).filter(SentimentAnalysis.article_id == article_id).first()


def create_sentiment_analysis(db: Session, analysis: SentimentAnalysisCreate):
    db_analysis = SentimentAnalysis(
        article_id=analysis.article_id,
        sentiment=analysis.sentiment,
        score=analysis.score
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis


def update_sentiment_analysis(db: Session, analysis_id: int, new_sentiment: str, new_score: float):
    sentiment_analysis = db.query(SentimentAnalysis).filter(SentimentAnalysis.article_id == analysis_id).first()
    if sentiment_analysis:
        sentiment_analysis.sentiment = new_sentiment
        sentiment_analysis.score = new_score
        db.commit()
        db.refresh(sentiment_analysis)
        return sentiment_analysis
    return None

