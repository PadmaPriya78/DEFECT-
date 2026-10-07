import os
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database import Base, engine, get_db
import models
import schemas
from auth import get_current_user, create_access_token, hash_password, verify_password
from github_analyzer import analyze_repository
from ml_predictor import is_model_ready

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DefectGuard AI", version="1.0.0")

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "model_ready": is_model_ready()}


# ── Auth ──────────────────────────────────────────────
@app.post("/auth/register", response_model=schemas.UserOut)
def register(email: str, password: str, name: str = "", db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        raise HTTPException(400, "Email already registered")
    user = models.User(email=email, name=name, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/auth/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not user.hashed_password or not verify_password(password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


# ── Analysis ──────────────────────────────────────────
def _run_analysis(analysis_id: str, repo_url: str, db: Session):
    analysis = db.query(models.Analysis).filter(models.Analysis.id == analysis_id).first()
    analysis.status = "running"
    db.commit()

    try:
        module_results = analyze_repository(repo_url)

        high = sum(1 for m in module_results if m["risk_level"] == "HIGH")
        medium = sum(1 for m in module_results if m["risk_level"] == "MEDIUM")
        low = sum(1 for m in module_results if m["risk_level"] == "LOW")

        for m in module_results:
            db.add(models.ModuleResult(analysis_id=analysis_id, **m))

        analysis.files_analyzed = len(module_results)
        analysis.high_risk_count = high
        analysis.medium_risk_count = medium
        analysis.low_risk_count = low
        analysis.status = "done"
        analysis.completed_at = datetime.utcnow()
    except Exception as e:
        analysis.status = "failed"
        analysis.error_message = str(e)

    db.commit()


@app.post("/analyze", response_model=schemas.AnalysisOut)
def analyze(
    req: schemas.AnalyzeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    analysis = models.Analysis(
        repo_url=req.repo_url,
        user_id=current_user.id if current_user else None,
        status="pending",
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    # runs synchronously for simplicity; swap for Celery task for large repos
    _run_analysis(analysis.id, req.repo_url, db)
    db.refresh(analysis)
    return analysis


@app.get("/analyze/{analysis_id}", response_model=schemas.AnalysisOut)
def get_analysis(analysis_id: str, db: Session = Depends(get_db)):
    analysis = db.query(models.Analysis).filter(models.Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(404, "Analysis not found")
    return analysis


@app.get("/analyses", response_model=list[schemas.AnalysisOut])
def list_analyses(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    q = db.query(models.Analysis)
    if current_user:
        q = q.filter(models.Analysis.user_id == current_user.id)
    return q.order_by(models.Analysis.created_at.desc()).limit(50).all()
