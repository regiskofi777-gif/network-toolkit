"""Logging pour le Network Toolkit"""

import logging
import sys

def setup_logger(name: str = "network_toolkit", level: int = logging.INFO) -> logging.Logger:
    
    logger = logging.getLogger(name)
    # Evite l'ajoute multiple de handler si setup_logger est appelé plusieurs fois
    if logger.handlers:
        return logger

    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)

    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger