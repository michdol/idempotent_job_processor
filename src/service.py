import asyncio
import random

from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional

from . import models, schemas, database


def get_available_worker(db: Session) -> models.Worker:
    """
    Get an available worker or create one if none exist.

    Args:
        db: The database session.

    Returns:
        A worker object.
    """
    worker = db.query(models.Worker).filter(
        models.Worker.status == models.WorkerStatus.AVAILABLE
    ).first()

    if not worker:
        worker = models.Worker()
        db.add(worker)
        db.commit()
        db.refresh(worker)

    return worker


async def check_existing_request(
    request: schemas.JobRequestCreate,
    db: Session = Depends(database.get_db)
) -> Optional[models.JobRequest]:
    """
    Dependency to check if a request with the given request_id already exists.

    Args:
        request: The job request to check.
        db: The database session.

    Returns:
        A job request object.
    """
    return db.query(models.JobRequest).filter(
        models.JobRequest.request_id == request.request_id
    ).first()


async def process_job_request(request_id: str, worker_id: int, db: Session):
    """
    Process a job request asynchronously.

    Args:
        request_id: The ID of the request to process.
        worker_id: The ID of the worker processing the request.
        db: The database session.
    """
    # Simulate some processing time
    await asyncio.sleep(2)
    
    result = random.randint(1, 100)
    
    request = db.query(models.JobRequest).filter(
        models.JobRequest.request_id == request_id
    ).first()

    if request:
        request.status = "completed"
        request.processed_at = datetime.now()
        request.result = {"random_number": result, "worker_id": worker_id}

        worker = db.query(models.Worker).filter(models.Worker.id == worker_id).first()
        if worker:
            worker.status = models.WorkerStatus.AVAILABLE
        db.commit()
