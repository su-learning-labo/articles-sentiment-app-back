import ginza
from fastapi import APIRouter, Body
from schemas import TextAnalysisResponse, TextAnalysisRequest
import spacy
from spacy.tokens import Token

nlp = spacy.load('ja_ginza_electra')
ginza.set_split_mode(nlp, 'C')

router = APIRouter()


@router.post("/analyze-text/", response_model=TextAnalysisResponse)
def analyze_text(request: TextAnalysisRequest = Body(...)):
    doc = nlp(request.text)
    nouns = [token.text for token in doc if Token.pos_ == 'NOUN']
    return TextAnalysisResponse(nouns=nouns)


