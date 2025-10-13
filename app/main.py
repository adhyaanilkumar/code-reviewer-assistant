from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
import os
import aiofiles

from .database import get_db, create_tables, CodeReview
from .models import CodeReviewResponse, CodeReviewRequest
from .llm_service import LLMCodeReviewer

app = FastAPI(title="Code Review Assistant", version="1.0.0")

# Create database tables
create_tables()

# Initialize LLM service
llm_reviewer = LLMCodeReviewer()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main dashboard"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/review", response_model=CodeReviewResponse)
async def review_code(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and review a code file
    """
    try:
        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Analyze code using LLM
        analysis = llm_reviewer.analyze_code(file.filename, content_str)
        
        # Create database record
        db_review = CodeReview(
            filename=file.filename,
            file_content=content_str,
            review_report=analysis["report"],
            readability_score=analysis["scores"]["readability_score"],
            modularity_score=analysis["scores"]["modularity_score"],
            bug_risk_score=analysis["scores"]["bug_risk_score"],
            overall_score=analysis["scores"]["overall_score"],
            suggestions="\n".join(analysis["suggestions"])
        )
        
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        
        return CodeReviewResponse(
            id=db_review.id,
            filename=db_review.filename,
            review_report=db_review.review_report,
            readability_score=db_review.readability_score,
            modularity_score=db_review.modularity_score,
            bug_risk_score=db_review.bug_risk_score,
            overall_score=db_review.overall_score,
            suggestions=db_review.suggestions,
            created_at=db_review.created_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/api/review-text", response_model=CodeReviewResponse)
async def review_code_text(
    request: CodeReviewRequest,
    db: Session = Depends(get_db)
):
    """
    Review code from text input
    """
    try:
        # Analyze code using LLM
        analysis = llm_reviewer.analyze_code(request.filename, request.content)
        
        # Create database record
        db_review = CodeReview(
            filename=request.filename,
            file_content=request.content,
            review_report=analysis["report"],
            readability_score=analysis["scores"]["readability_score"],
            modularity_score=analysis["scores"]["modularity_score"],
            bug_risk_score=analysis["scores"]["bug_risk_score"],
            overall_score=analysis["scores"]["overall_score"],
            suggestions="\n".join(analysis["suggestions"])
        )
        
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        
        return CodeReviewResponse(
            id=db_review.id,
            filename=db_review.filename,
            review_report=db_review.review_report,
            readability_score=db_review.readability_score,
            modularity_score=db_review.modularity_score,
            bug_risk_score=db_review.bug_risk_score,
            overall_score=db_review.overall_score,
            suggestions=db_review.suggestions,
            created_at=db_review.created_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing code: {str(e)}")

@app.get("/api/reviews", response_model=List[CodeReviewResponse])
async def get_reviews(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all code reviews
    """
    reviews = db.query(CodeReview).offset(skip).limit(limit).all()
    return [
        CodeReviewResponse(
            id=review.id,
            filename=review.filename,
            review_report=review.review_report,
            readability_score=review.readability_score,
            modularity_score=review.modularity_score,
            bug_risk_score=review.bug_risk_score,
            overall_score=review.overall_score,
            suggestions=review.suggestions,
            created_at=review.created_at
        )
        for review in reviews
    ]

@app.get("/api/reviews/{review_id}", response_model=CodeReviewResponse)
async def get_review(
    review_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific code review by ID
    """
    review = db.query(CodeReview).filter(CodeReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return CodeReviewResponse(
        id=review.id,
        filename=review.filename,
        review_report=review.review_report,
        readability_score=review.readability_score,
        modularity_score=review.modularity_score,
        bug_risk_score=review.bug_risk_score,
        overall_score=review.overall_score,
        suggestions=review.suggestions,
        created_at=review.created_at
    )

@app.delete("/api/reviews/{review_id}")
async def delete_review(
    review_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a code review
    """
    review = db.query(CodeReview).filter(CodeReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Code Review Assistant"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
