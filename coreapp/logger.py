import logging
import os

def setup_logger(module_name: str, log_file: str, log_dir: str = 'Logs') -> logging.Logger:
 
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, log_file)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path)
        ]
    )

    # Get the logger
    logger = logging.getLogger(module_name)
    
    return logger
