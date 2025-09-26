# backend/utils/job_queue.py
import queue
import threading
import uuid
import time
from typing import Dict, Any, Optional
from utils.logger import get_logger

logger = get_logger(__name__)

# In-memory job queue + status store
job_queue: queue.Queue = queue.Queue()
job_status: Dict[str, Dict[str, Any]] = {}

def enqueue_job(func, *args, **kwargs) -> str:
    """Add job to queue and return job_id"""
    job_id = str(uuid.uuid4())
    job_status[job_id] = {"status": "queued", "result": None}
    job_queue.put((job_id, func, args, kwargs))
    logger.info(f"Job {job_id} enqueued for {func.__name__}")
    return job_id


def get_job_status(job_id: str) -> Dict[str, Any]:
    """Return status + result of a job"""
    return job_status.get(job_id, {"status": "not_found"})


def worker():
    """Background worker to process jobs"""
    while True:
        try:
            job_id, func, args, kwargs = job_queue.get()
            job_status[job_id]["status"] = "running"
            logger.info(f"Job {job_id} started: {func.__name__}")
            result = func(*args, **kwargs)
            job_status[job_id]["status"] = "completed"
            job_status[job_id]["result"] = result
            logger.info(f"Job {job_id} completed")
        except Exception as e:
            job_status[job_id]["status"] = "failed"
            job_status[job_id]["result"] = str(e)
            logger.error(f"Job {job_id} failed: {e}")
        finally:
            job_queue.task_done()


def start_worker(num_workers: int = 2):
    """Start worker threads"""
    for _ in range(num_workers):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        logger.info("Worker thread started")


# Streaming Generator (for SSE responses)
def stream_response(job_id: str):
    """Yield job status updates for streaming endpoints"""
    last_status = None
    while True:
        status = job_status.get(job_id)
        if not status:
            yield f"data: {{\"status\":\"not_found\"}}\n\n"
            break

        if status["status"] != last_status:
            yield f"data: {status}\n\n"
            last_status = status["status"]

        if status["status"] in ["completed", "failed"]:
            break
        time.sleep(1)
