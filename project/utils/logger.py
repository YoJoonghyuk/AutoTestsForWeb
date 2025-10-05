import logging
import os

def setup_logger(log_file="test.log", level=logging.INFO):
    """
    Настраивает логгер.
    """
    log_dir = "logs"  
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  
    log_file_path = os.path.join(log_dir, log_file)  

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    file_handler = logging.FileHandler(log_file_path, mode='w')
    file_handler.setFormatter(formatter)


    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(level) 
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger  

logger = setup_logger()  
