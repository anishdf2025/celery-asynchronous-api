import time
from celery import shared_task

@shared_task(bind=True, name="multiply_numbers")
def multiply_numbers(self, x: float, y: float) -> float:
    """
    Multiply two numbers with a 5-minute delay.
    
    Args:
        x: First number
        y: Second number
        
    Returns:
        The product of x and y
    """
    # Log that task has started
    self.update_state(state="PROGRESS", meta={"message": "Task has started"})
    
    # Simulate a long-running task with a 10-second delay (changed from 5 minutes for testing)
    time.sleep(30)  # 10 seconds instead of 300 (5 minutes)
    
    # Calculate the result
    result = x * y
    
    return result
