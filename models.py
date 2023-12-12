from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class NewsArticle(Base):
    __tablename__ = 'news_articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    url = Column(String)
    published_at = Column(DateTime)
    source_name = Column(String)
    fetched_at = Column(DateTime, default=datetime.now())
    ranking = Column(Integer)

    sentiments = relationship("SentimentAnalysis", back_populates="article")


class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analysis"

    id = Column(Integer, primary_key=True, index=True)
    sentiment = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    article_id = Column(Integer, ForeignKey('news_articles.id'), nullable=False)
    # analyzed_description = Column(String)

    article = relationship("NewsArticle", back_populates="sentiments")

