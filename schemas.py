from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


# 共通となる記事の属性
class NewsArticleBase(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    published_at: datetime
    source_name: str
    ranking: int


# ニュース記事の作成用スキーマ（ベースモデルを継承）
class NewsArticleCreate(NewsArticleBase):
    pass


# ニュース記事の読み込み用スキーマ（ベースモデルを継承）
class NewsArticle(NewsArticleBase):
    id: int
    fetched_at: datetime

    class Config:
        from_attributes = True


# 共通の感情分析属性
class SentimentAnalysisBase(BaseModel):
    sentiment: str
    score: float


# 感情分析結果の作成用スキーマ
class SentimentAnalysisCreate(SentimentAnalysisBase):
    article_id: int


# 感情分析結果の読み込み用スキーマ
class SentimentAnalysis(SentimentAnalysisBase):
    id: int
    article_id: int

    class Config:
        from_attributes = True


# 感情分析の更新用スキーマ
class SentimentAnalysisUpdate(BaseModel):
    sentiment: str
    score: float


# ニュース記事とそれに紐づく感情分析結果の読み込み用スキーマ
class NewsArticleWithSentiment(NewsArticle):
    sentiments: List[SentimentAnalysis] = []


class TextAnalysisRequest(BaseModel):
    text: str


class TextAnalysisResponse(BaseModel):
    nouns: List[str]
