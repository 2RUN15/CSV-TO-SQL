import logging

def log_al(name: str,dosya: str = "log.log") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        dosya_handler = logging.FileHandler(dosya)
        dosya_handler.setLevel(logging.DEBUG)

        terminal_handler = logging.StreamHandler()
        terminal_handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        dosya_handler.setFormatter(formatter)
        terminal_handler.setFormatter(formatter)

        logger.addHandler(terminal_handler)
        logger.addHandler(dosya_handler)
    
    return logger