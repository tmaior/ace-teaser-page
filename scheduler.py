import time
import logging
import sys
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("scheduler_service")

def check_webapp_health():
    health_check_url = "http://127.0.0.1:8000/health"
    try:
        # Make a GET request to the health check URL with a timeout.
        response = requests.get(health_check_url, timeout=5) # 5-second timeout

        # Check if the request was successful (status code 200-299)
        if response.ok:
            logger.info(f"HEALTH CHECK: Web app is healthy. Status: {response.status_code}")
        else:
            # Log a warning if the status code indicates an error
            logger.warning(f"HEALTH CHECK: Web app responded with an error. Status: {response.status_code}, Response: {response.text[:200]}")

    except requests.exceptions.Timeout:
        # Log an error if the request times out
        logger.error(f"HEALTH CHECK: Web app health check timed out at {health_check_url}")
    except requests.exceptions.ConnectionError:
        # Log an error if the connection fails (e.g., app is down)
        logger.error(f"HEALTH CHECK: Failed to connect to web app at {health_check_url}. Is it running?")
    except requests.exceptions.RequestException as e:
        # Log any other request-related errors
        logger.error(f"HEALTH CHECK: An error occurred during web app health check: {e}")

if __name__ == '__main__':
    scheduler = BlockingScheduler(logger=logger)
    scheduler.add_job(
        check_webapp_health,    # The function to execute
        'interval',             # Trigger type
        minutes=1,              # Interval
        id="webapp_health_check_job", # Unique ID for the job
        replace_existing=True   # Replace if a job with this ID already exists
    )

    logger.info("Scheduler initialized with webapp health check. Starting now...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")
