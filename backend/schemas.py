from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl


class AnalyzeRequest(BaseModel):
    repo_url: str


class ModuleResultOut(BaseModel):
    file_path: str
    loc: int
    complexity: float
    num_functions: int
    num_classes: int
    num_imports: int
    comment_ratio: float
    defect_probability: float
    risk_level: str
    flag_reason: Optional[str] = None

    class Config:
        from_attributes = True


class AnalysisOut(BaseModel):
    id: str
    repo_url: str
    status: str
    files_analyzed: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    modules: List[ModuleResultOut] = []

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: str
    email: str
    name: Optional[str] = None

    class Config:
        from_attributes = True
