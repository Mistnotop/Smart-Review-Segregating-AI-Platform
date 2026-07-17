import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="hf-inference",
    api_key=os.getenv("HF_TOKEN")
)

MODEL = "distilbert-base-uncased-finetuned-sst-2-english"


def analyze_sentiment(review: str):
    result = client.text_classification(
        review,
        model=MODEL
    )

    return {
        "sentiment": result.label.capitalize(),
        "confidence": round(result.score, 4)
    }