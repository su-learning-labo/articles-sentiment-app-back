import ginza
from fastapi import APIRouter, Body
from schemas import TextAnalysisResponse, TextAnalysisRequest, TokenData, NounsResponse, TextResponse, TextRequest
import spacy


nlp = spacy.load('ja_ginza_electra')
router = APIRouter()


@router.post("/analyze-text/", response_model=TextAnalysisResponse)
def analyze_text(request: TextAnalysisRequest = Body(...)):
    doc = nlp(request.text)
    ginza.set_split_mode(nlp, 'C')
    tokens = [
        TokenData(
            token_no=str(i),
            text=token.text,
            lemma=token.lemma_,
            pos=token.pos_,
            tag=token.tag_
        ) for i, token in enumerate(doc)
    ]
    return TextAnalysisResponse(tokens=tokens)


@router.post('/wakati/', response_model=TextResponse)
def create_wakati(request: TextRequest):
    doc = nlp(request.text)
    ginza.set_split_mode(nlp, 'C')
    wakati = ' '.join([token.text for token in doc])

    return TextResponse(wakati=wakati)


@router.post("/extract-nouns/", response_model=NounsResponse)
def extract_noun(request: TextAnalysisRequest = Body(...)):
    doc = nlp(request.text)
    nouns = [token.text for token in doc if token.pos_ == 'NOUN']
    return NounsResponse(nouns=nouns)
