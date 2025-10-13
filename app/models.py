from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CodeReviewRequest(BaseModel):
    filename: str
    content: str

class CodeReviewResponse(BaseModel):
    id: int
    filename: str
    review_report: str
    readability_score: float
    modularity_score: float
    bug_risk_score: float
    overall_score: float
    suggestions: str
    created_at: datetime

class ReviewScores(BaseModel):
    readability_score: float
    modularity_score: float
    bug_risk_score: float
    overall_score: float

class ReviewReport(BaseModel):
    report: str
    scores: ReviewScores
    suggestions: List[str]
