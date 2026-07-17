import re


def detect_fake_review(review: str) -> bool:
    text = review.lower()

    suspicious_words = [
        "buy now",
        "100% guaranteed",
        "guaranteed",
        "limited offer",
        "click here",
        "best ever",
        "must buy",
        "free gift",
        "winner",
        "act now"
    ]

    # Check suspicious phrases
    for word in suspicious_words:
        if word in text:
            return True

    # Check repeated words
    words = text.split()

    for word in set(words):
        if words.count(word) >= 4:
            return True

    # Too many exclamation marks
    if review.count("!") >= 5:
        return True

    # Too many stars
    if review.count("⭐") >= 5:
        return True

    return False