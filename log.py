import logging


def logs(file_name):
    """
    Returns a logger that allows logging in the console and in a file
    """

    # Basic logger configuration
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.DEBUG)

    # Create a handler for files
    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(logging.INFO)  # This handler only handles logs of INFO level and higher.

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # This handler handles all log levels

    # Formatter to add timestamps to log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Assign formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
