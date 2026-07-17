from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


def analyze_sentiment(review: str):
    result = classifier(review)[0]

    return {
        "sentiment": result["label"].capitalize(),
        "confidence": round(result["score"], 4)
    }