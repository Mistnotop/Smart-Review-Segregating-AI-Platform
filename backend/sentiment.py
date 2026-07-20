from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(review: str):
    scores = analyzer.polarity_scores(review)

    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    confidence = abs(compound)

    return {
        "sentiment": sentiment,
        "confidence": round(confidence * 100, 2)
    }