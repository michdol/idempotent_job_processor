from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from . import models, schemas, service, database


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Job Request Processing API",
    description="API for processing job requests with worker assignment",
    version="1.0.0"
)


@app.post("/process-request", response_model=schemas.JobRequestResponse)
async def process_request(
    request: schemas.JobRequestCreate,
    background_tasks: BackgroundTasks,
    existing_request: models.JobRequest | None = Depends(service.check_existing_request),
    db: Session = Depends(database.get_db)
):
    if existing_request:
        return existing_request

    db_request = models.JobRequest(
        request_id=request.request_id,
        payload=request.payload,
        status="pending"
    )

    worker = service.get_available_worker(db)
    db_request.worker_id = worker.id
    db_request.status = "processing"

    worker.status = models.WorkerStatus.BUSY

    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    background_tasks.add_task(
        service.process_job_request,
        request.request_id,
        worker.id,
        db
    )

    return db_request


@app.get("/requests", response_model=list[schemas.JobRequestResponse])
def get_requests(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    Additional endpoint to fetch all requests.
    """
    requests = db.query(models.JobRequest).offset(skip).limit(limit).all()
    return requests 
