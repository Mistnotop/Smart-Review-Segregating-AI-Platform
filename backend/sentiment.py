from transformers import pipeline

classifier = None


def get_classifier():
    global classifier
    if classifier is None:
        classifier = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
    return classifier


def analyze_sentiment(review: str):
    model = get_classifier()
    result = model(review)[0]

    return {
        "sentiment": result["label"].capitalize(),
        "confidence": round(result["score"], 4)
    }