# logger.py
import logging
import os
from datetime import datetime
import traceback
import sys

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging with more detailed format
logging.basicConfig(
    filename=f'logs/app_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_event(message, include_trace=False):
    """
    Log an informational event
    Args:
        message: The message to log
        include_trace: Whether to include the stack trace
    """
    # Get caller frame info
    frame = sys._getframe(1)
    caller = f"{frame.f_code.co_filename}:{frame.f_lineno}"
    
    # Log with caller information
    full_message = f"[{caller}] {message}"
    logging.info(full_message)
    
    if include_trace:
        stack = ''.join(traceback.format_stack()[:-1])
        logging.info(f"Stack trace:\n{stack}")
    
    # Also print to console for debugging
    print(f"Event: {message}")

def log_error(message, exc_info=None):
    """
    Log an error with full stack trace
    Args:
        message: The error message
        exc_info: Exception information (optional)
    """
    # Get caller frame info
    frame = sys._getframe(1)
    caller = f"{frame.f_code.co_filename}:{frame.f_lineno}"
    
    # Log with caller information
    full_message = f"[{caller}] ERROR: {message}"
    
    if exc_info:
        logging.error(full_message, exc_info=exc_info)
        # Also log the full traceback
        logging.error(f"Full traceback:\n{''.join(traceback.format_tb(exc_info.__traceback__))}")
    else:
        logging.error(full_message)
        # Log current stack trace
        stack = ''.join(traceback.format_stack()[:-1])
        logging.error(f"Stack trace:\n{stack}")
    
    # Also print to console for debugging
    print(f"Error: {message}")

def log_debug(message):
    """Log debug information"""
    # Get caller frame info
    frame = sys._getframe(1)
    caller = f"{frame.f_code.co_filename}:{frame.f_lineno}"
    
    # Log with caller information
    full_message = f"[{caller}] DEBUG: {message}"
    logging.debug(full_message)
    
    # Also print to console for debugging
    print(f"Debug: {message}")

def get_last_logs(n=10):
    """
    Retrieve the last n log entries
    Args:
        n: Number of log entries to retrieve
    Returns:
        List of last n log entries
    """
    try:
        with open(logging.getLoggerClass().root.handlers[0].baseFilename, 'r') as f:
            logs = f.readlines()
            return logs[-n:]
    except Exception as e:
        print(f"Error retrieving logs: {str(e)}")
        return []
