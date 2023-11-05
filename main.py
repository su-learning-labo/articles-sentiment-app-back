from fastapi import FastAPI

from routers import news
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(news.router)


@app.get("/")
def get_root():
    return {'message': 'Welcome to Sentiment-App!'}
