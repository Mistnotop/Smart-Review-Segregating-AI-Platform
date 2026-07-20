import os
from huggingface_hub import InferenceClient

MODEL = "distilbert-base-uncased-finetuned-sst-2-english"

client = InferenceClient(
    token=os.getenv("HF_TOKEN")
)


def analyze_sentiment(review: str):
    try:
        result = client.text_classification(
            review,
            model=MODEL
        )

        return {
            "sentiment": result.label.capitalize(),
            "confidence": round(result.score, 4)
        }

    except Exception as e:
        print("Sentiment Error:", e)
        return {
            "sentiment": "Unknown",
            "confidence": 0.0
        }