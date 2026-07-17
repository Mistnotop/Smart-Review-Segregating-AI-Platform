from fastapi import FastAPI
from typing import List
from schemas import ReviewRequest, ReviewResponse, ReviewOut
from sentiment import analyze_sentiment
from fake_detector import detect_fake_review
from database import SessionLocal
from crud import save_review, get_reviews
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SmartReview AI API",
    description="AI-powered sentiment analysis and fake review detection.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://smart-review-segregating-ai-platfor.vercel.app/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to SmartReview AI"
    }


@app.post("/analyze", response_model=ReviewResponse)
def analyze(data: ReviewRequest):

    sentiment_result = analyze_sentiment(data.review)

    fake_result = detect_fake_review(data.review)

    db = SessionLocal()

    save_review(
        db,
        data.review,
        sentiment_result["sentiment"],
        sentiment_result["confidence"],
        fake_result
    )

    db.close()

    return {
        "review": data.review,
        "sentiment": sentiment_result["sentiment"],
        "confidence": sentiment_result["confidence"],
        "fake": fake_result
    }

@app.get("/reviews", response_model=List[ReviewOut])
def reviews():

    db = SessionLocal()

    data = get_reviews(db)

    db.close()

    return data