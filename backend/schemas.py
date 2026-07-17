from pydantic import BaseModel, ConfigDict


# Request model (input from user)
class ReviewRequest(BaseModel):
    review: str


# Response model for POST /analyze
class ReviewResponse(BaseModel):
    review: str
    sentiment: str
    confidence: float
    fake: bool


# Response model for GET /reviews
class ReviewOut(BaseModel):
    id: int
    review: str
    sentiment: str
    confidence: float
    fake: bool

    model_config = ConfigDict(from_attributes=True)