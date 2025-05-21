import pytest

from sqlalchemy.orm import Session
from unittest.mock import Mock, patch

from src import models, schemas, service


@pytest.fixture
def mock_db():
    return Mock(spec=Session)


@pytest.fixture
def mock_worker():
    worker = Mock(spec=models.Worker)
    worker.id = 1
    worker.status = models.WorkerStatus.AVAILABLE
    return worker


@pytest.fixture
def mock_job_request():
    request = Mock(spec=models.JobRequest)
    request.id = 1
    request.request_id = "test123"
    request.payload = {"test": "data"}
    request.status = "pending"
    request.worker_id = None
    request.processed_at = None
    request.result = None
    return request


def test_get_available_worker_existing(mock_db, mock_worker):
    """
    Test getting an existing available worker.
    """
    mock_db.query.return_value.filter.return_value.first.return_value = mock_worker
    result = service.get_available_worker(mock_db)

    assert result == mock_worker
    mock_db.query.assert_called_once_with(models.Worker)
    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()


def test_get_available_worker_new(mock_db, mock_worker):
    """
    Test creating a new worker when none are available.
    """
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.add.return_value = None
    mock_db.refresh.side_effect = lambda x: setattr(x, 'id', 1)

    result = service.get_available_worker(mock_db)

    assert isinstance(result, models.Worker)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_check_existing_request_found(mock_db, mock_job_request):
    """
    Test finding an existing request.
    """
    mock_db.query.return_value.filter.return_value.first.return_value = mock_job_request
    request = schemas.JobRequestCreate(request_id="test123", payload={"test": "data"})

    result = await service.check_existing_request(request, mock_db)

    assert result == mock_job_request
    mock_db.query.assert_called_once_with(models.JobRequest)


@pytest.mark.asyncio
async def test_check_existing_request_not_found(mock_db):
    """
    Test not finding an existing request.
    """
    mock_db.query.return_value.filter.return_value.first.return_value = None
    request = schemas.JobRequestCreate(request_id="test123", payload={"test": "data"})

    result = await service.check_existing_request(request, mock_db)

    assert result is None
    mock_db.query.assert_called_once_with(models.JobRequest)


@pytest.mark.asyncio
@patch("src.service.asyncio.sleep")
async def test_process_job_request(mock_sleep, mock_db, mock_job_request, mock_worker):
    """
    Test processing a job request.

    Mock sleep to speed up the test.
    """
    mock_db.query.return_value.filter.return_value.first.side_effect = [mock_job_request, mock_worker]
    request_id = "test123"
    worker_id = 1

    await service.process_job_request(request_id, worker_id, mock_db)

    assert mock_job_request.status == "completed"
    assert mock_job_request.processed_at is not None
    assert isinstance(mock_job_request.result, dict)
    assert "random_number" in mock_job_request.result
    assert mock_job_request.result["worker_id"] == worker_id
    assert mock_worker.status == models.WorkerStatus.AVAILABLE
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
@patch("src.service.asyncio.sleep")
async def test_process_job_request_not_found(mock_sleep, mock_db):
    """
    Test processing a non-existent job request.

    Mock sleep to speed up the test.
    """
    mock_db.query.return_value.filter.return_value.first.return_value = None
    request_id = "nonexistent"
    worker_id = 1

    await service.process_job_request(request_id, worker_id, mock_db)

    mock_db.commit.assert_not_called() 
