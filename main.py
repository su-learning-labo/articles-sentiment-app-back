from fastapi import FastAPI

from routers import news, nlp_routers
from database import Base, engine

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn.error")

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(news.router)
app.include_router(nlp_routers.router)


@app.get("/")
def get_root():
    return {'message': 'Welcome to Sentiment-App!'}
