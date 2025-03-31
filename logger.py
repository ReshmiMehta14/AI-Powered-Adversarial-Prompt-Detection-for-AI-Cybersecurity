import logging
import os

LOG_FILE_PATH = 'logs/prompt_detection.log'

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

# Configure a single logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Avoid adding multiple handlers
if not logger.hasHandlers():
    handler = logging.FileHandler(LOG_FILE_PATH)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - User Input: %(message)s | Detection Result: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def log_detection(user_input, detection_result):
    # Ensure HTTP requests are excluded
    if "HTTP Request" in user_input or "HTTP Request" in detection_result:
        print("⛔ Skipping API-related log.")
        return

    # Deduplicate entries
    detection_result_cleaned = detection_result.split("|")[0].strip()

    try:
        log_message = f"User Input: {user_input} | Detection Result: {detection_result_cleaned}"

        # Log using logger instead of basicConfig
        logger.info(log_message)
        print("✅ Log Saved:", log_message)
    except Exception as e:
        print(f"❌ Error Logging Data: {str(e)}")
