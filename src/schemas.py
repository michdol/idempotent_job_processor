from datetime import datetime
from pydantic import BaseModel
from typing import Any


class JobRequestBase(BaseModel):
    request_id: str
    payload: dict[str, Any]


class JobRequestCreate(JobRequestBase):
    pass


class JobRequestResponse(JobRequestBase):
    id: int
    worker_id: int | None = None
    status: str
    created_at: datetime
    processed_at: datetime | None = None
    result: dict[str, Any] | None = None
