from sqlalchemy.orm import Session
from datetime import datetime
from models import NewsArticle, SentimentAnalysis
from schemas import NewsArticleCreate, SentimentAnalysisCreate
# from services.news_service import analyze_sentiment


def get_news(db: Session, news_id: int):
    return db.query(NewsArticle).filter(NewsArticle.id == news_id).first()


def get_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(NewsArticle).offset(skip).limit(limit).all()


# def get_news_by_ranking(db: Session, ranking: int):
#     return db.query(NewsArticle).filter(NewsArticle.ranking == ranking).first()


def create_news_article(db: Session, news: NewsArticleCreate):
    db_news = NewsArticle(**news.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


def get_sentiment_analysis(db: Session, analysis_id: int):
    return db.query(SentimentAnalysis).filter(SentimentAnalysis.id == analysis_id).first()


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


def update_sentiment_analysis(db: Session, analysis_id: int, sentiment: str, score: float):
    db_analysis = get_sentiment_analysis(db, analysis_id)
    if db_analysis:
        db_analysis.sentiment = sentiment
        db_analysis.score = score
        db.commit()
        db.refresh(db_analysis)
    return db_analysis


# def analyze_article_sentiment(db: Session, article_id: int):
#     article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
#     if not article:
#         return None
#
#     # 記事の内容に対して感情分析を実行
#     sentiment, score = analyze_sentiment(article.description)
#
#     # 感情分析結果をデータベースに保存
#     sentiment_analysis = SentimentAnalysis(
#         article_id=article_id,
#         sentiment=sentiment,
#         score=score
#     )
#     db.add(sentiment_analysis)
#     db.commit()
#     db.refresh(sentiment_analysis)
#     return sentiment_analysis
#
#
# def analyze_and_update(db: Session, article_id: int):
#     # 特定の記事を取得
#     article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
#     if not article:
#         return None  # またはエラーを投げる
#
#     # 記事の説明から感情分析を行う
#     sentiment, score = analyze_sentiment(article.description)
#
#     # 既存の感情分析結果を取得、または新しく作成する
#     sentiment_analysis = db.query(SentimentAnalysis).filter(SentimentAnalysis.article_id == article_id).first()
#     if sentiment_analysis:
#         # 既存の感情分析結果を更新
#         sentiment_analysis.sentiment = sentiment
#         sentiment_analysis.score = score
#     else:
#         # 新しい感情分析結果を作成
#         sentiment_analysis = SentimentAnalysis(article_id=article_id, sentiment=sentiment, score=score)
#         db.add(sentiment_analysis)
#
#     db.commit()
#     return sentiment_analysis
