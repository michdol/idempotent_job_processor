# Job Request Processing API

A FastAPI application that processes job requests, ensuring each request is processed only once and assigned to one of three workers.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the application:
```bash
uvicorn src.main:app --reload
```

4. Run tests:
```
pytest tests/
```

The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc
