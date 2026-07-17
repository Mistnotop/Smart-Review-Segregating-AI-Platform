from sqlalchemy.orm import Session
import models


def save_review(db: Session, review, sentiment, confidence, fake):

    new_review = models.Review(
        review=review,
        sentiment=sentiment,
        confidence=confidence,
        fake=fake
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    print("Saved Review ID:", new_review.id)

    return new_review


def get_reviews(db: Session):
    return db.query(models.Review).all()