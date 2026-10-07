import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base


def gen_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    google_sub = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    analyses = relationship("Analysis", back_populates="user")


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    repo_url = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, running, done, failed
    files_analyzed = Column(Integer, default=0)
    high_risk_count = Column(Integer, default=0)
    medium_risk_count = Column(Integer, default=0)
    low_risk_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="analyses")
    modules = relationship("ModuleResult", back_populates="analysis", cascade="all, delete-orphan")


class ModuleResult(Base):
    __tablename__ = "module_results"

    id = Column(String, primary_key=True, default=gen_uuid)
    analysis_id = Column(String, ForeignKey("analyses.id"), nullable=False)
    file_path = Column(String, nullable=False)
    loc = Column(Integer, default=0)
    complexity = Column(Float, default=0.0)
    num_functions = Column(Integer, default=0)
    num_classes = Column(Integer, default=0)
    num_imports = Column(Integer, default=0)
    comment_ratio = Column(Float, default=0.0)
    defect_probability = Column(Float, default=0.0)
    risk_level = Column(String, default="LOW")  # HIGH, MEDIUM, LOW
    flag_reason = Column(Text, nullable=True)

    analysis = relationship("Analysis", back_populates="modules")
