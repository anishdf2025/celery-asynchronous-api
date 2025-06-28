from fastapi import APIRouter, HTTPException, status
from app.schemas.request_models import MultiplicationRequest, TaskSubmitResponse, TaskStatusResponse
from app.tasks.math_tasks import multiply_numbers
from app.core.celery_app import celery_app
from celery.result import AsyncResult

router = APIRouter()

@router.post("/multiply", 
             response_model=TaskSubmitResponse, 
             status_code=status.HTTP_202_ACCEPTED,
             summary="Multiply two numbers asynchronously",
             description="Submit a task to multiply two numbers with a 5-minute delay")
async def multiply(request: MultiplicationRequest):
    """
    Endpoint to submit a multiplication task.
    
    Returns a task ID that can be used to check the status of the task.
    """
    # Submit the task to Celery
    task = multiply_numbers.delay(request.x, request.y)
    
    # Return the task ID and status
    return TaskSubmitResponse(
        task_id=task.id,
        status="Processing",
        message="Task has been submitted successfully"
    )

@router.get("/tasks/{task_id}", 
            response_model=TaskStatusResponse,
            summary="Check the status of a task",
            description="Get the current status and result of a previously submitted task")
async def get_task_status(task_id: str):
    """
    Endpoint to check the status of a previously submitted task.
    
    Returns the task status and result if the task is complete.
    """
    # Get the task result from Celery
    task_result = AsyncResult(task_id, app=celery_app)
    
    # Create response based on task state
    response = TaskStatusResponse(
        task_id=task_id,
        status=task_result.state
    )
    
    # Set HTTP status code based on task state
    http_status = status.HTTP_200_OK
    
    if task_result.state == "PENDING":
        # Task is still pending
        http_status = status.HTTP_202_ACCEPTED
    elif task_result.state == "SUCCESS":
        # Task is complete, include the result
        response.result = task_result.result
    elif task_result.state in ["FAILURE", "REVOKED"]:
        # Task failed or was revoked
        http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        response.error = str(task_result.result) if task_result.result else "Task failed"
    
    return response
