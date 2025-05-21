import enum

from sqlalchemy import Column, String, JSON, Integer, DateTime, Enum
from sqlalchemy.orm import declarative_base
from datetime import datetime


Base = declarative_base()


class WorkerStatus(enum.Enum):
    AVAILABLE = "available"
    BUSY = "busy"


class JobRequest(Base):
    __tablename__ = "job_requests"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True, nullable=False)
    payload = Column(JSON, nullable=False)
    worker_id = Column(Integer, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.now)
    processed_at = Column(DateTime, nullable=True)
    result = Column(JSON, nullable=True)


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(WorkerStatus), default=WorkerStatus.AVAILABLE)
    last_heartbeat = Column(DateTime, default=datetime.now) 
