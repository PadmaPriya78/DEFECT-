# DefectGuard AI

GitHub repository software defect & risk analyzer. Paste a repo URL, get every
source file classified HIGH / MEDIUM / LOW risk based on a trained defect-prediction model.

## Structure

```
backend/    FastAPI + SQLAlchemy + GitPython + scikit-learn/XGBoost
frontend/   React + Vite + Tailwind + Recharts
train_model.py   standalone training script (run separately, outputs feed backend/ml_artifacts/)
```

## Run with Docker

```bash
docker compose up --build
```

Frontend: http://localhost:5173
Backend:  http://localhost:8000

## Run locally (no Docker)

**Backend**
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit DATABASE_URL etc.
uvicorn main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

## Wiring in the trained model

`train_model.py` (project root) saves `best_model.pkl`, `scaler.pkl`,
`feature_columns.pkl`. Drop all three into `backend/ml_artifacts/`.
Until they're present, the backend falls back to a transparent heuristic
score (`ml_predictor.py::_heuristic_probability`) so the app runs end-to-end
without blocking on training.

**Important:** the feature schema the model was trained on must match
`feature_extractor.py`'s output (`loc`, `complexity`, `num_functions`,
`num_classes`, `num_imports`, `comment_ratio`). If the Kaggle dataset's real
columns differ, either rename/derive to match, or update `feature_extractor.py`
to emit the dataset's actual feature set — the two must agree exactly.

## Auth

JWT + password auth is wired (`/auth/register`, `/auth/login`). Google OAuth
client is referenced in `.env.example` (`GOOGLE_CLIENT_ID/SECRET`) but the
callback route isn't implemented yet — add an `/auth/google/callback` route
using `authlib` if needed; the User model already has a `google_sub` column.

## Known simplifications (flag before "production")

- Analysis runs synchronously in the request (`_run_analysis` in `main.py`).
  Celery/Redis are in requirements.txt but not wired — swap in for large repos.
- Feature extraction is regex-heuristic, not a real AST/tree-sitter parse.
  Same output schema either way, so upgrading it won't require model retraining.
- No rate limiting / repo-size cap on `/analyze` yet.
