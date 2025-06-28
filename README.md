# Asynchronous API with Celery and Redis

This project demonstrates an asynchronous API built with FastAPI, Celery, and Redis. The API performs multiplication of two numbers with a 5-minute delay to simulate a long-running task.

## Features

- FastAPI-based REST API
- Celery for task queue management
- Redis as message broker and result backend
- Asynchronous task processing
- Task status tracking with appropriate HTTP status codes

## Project Structure

```
celary+asynchronusapi/
├── .env                    # Environment variables
├── requirements.txt        # Project dependencies
├── app/                    # Main application package
│   ├── __init__.py         # Package initializer
│   ├── main.py             # FastAPI application entry point
│   ├── api/                # API routes
│   │   ├── __init__.py
│   │   └── endpoints.py    # API endpoints
│   ├── core/               # Core application code
│   │   ├── __init__.py
│   │   ├── config.py       # Configuration settings
│   │   └── celery_app.py   # Celery application setup
│   ├── tasks/              # Celery tasks
│   │   ├── __init__.py
│   │   └── math_tasks.py   # Mathematical operations tasks
│   └── schemas/            # Pydantic models
│       ├── __init__.py
│       └── request_models.py # Request/response schemas
```

## Getting Started

### Prerequisites

- Python 3.8+
- Redis

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Make sure Redis is running on your machine

### Running the Application

1. Start the FastAPI server:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. Start the Celery worker:
   ```
   celery -A app.core.celery_app worker --loglevel=info
   ```

## API Usage

### Multiply Two Numbers

**Endpoint**: `POST /api/multiply`

**Request Body**:
```json
{
  "x": 10,
  "y": 20
}
```

**Response**:
- Status Code: 202 Accepted
- Body:
```json
{
  "task_id": "task-uuid-here",
  "status": "Processing",
  "message": "Task has been submitted successfully"
}
```

### Check Task Status

**Endpoint**: `GET /api/tasks/{task_id}`

**Response**:
- If pending:
  - Status Code: 202 Accepted
  - Body:
  ```json
  {
    "task_id": "task-uuid-here",
    "status": "PENDING",
    "result": null
  }
  ```
- If completed:
  - Status Code: 200 OK
  - Body:
  ```json
  {
    "task_id": "task-uuid-here",
    "status": "SUCCESS",
    "result": 200
  }
  ```
- If failed:
  - Status Code: 500 Internal Server Error
  - Body:
  ```json
  {
    "task_id": "task-uuid-here",
    "status": "FAILURE",
    "error": "Error message here"
  }
  ```
