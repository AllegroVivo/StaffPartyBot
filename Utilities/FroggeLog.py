from __future__ import annotations

import logging
from logging import Formatter, FileHandler, StreamHandler
################################################################################
class FullDataFormatter(Formatter):

    def __init__(self):

        super().__init__(
            fmt=(
                "%(asctime)s - %(name)10s::%(levelname)-8s - %(message)s"
            ),
            datefmt="%m/%d/%y %H:%M:%S"
        )

################################################################################
class StreamDataFormatter(Formatter):

    def __init__(self):

        super().__init__(
            fmt="%(asctime)s - %(name)s::%(levelname)s - %(message)s",
            datefmt="%m/%d/%y %H:%M:%S"
        )

################################################################################
class _FroggeLog:

    _FDF = FullDataFormatter()
    _SDF = StreamDataFormatter()

    _FH = FileHandler("log.log", "w")
    _SH = StreamHandler()

################################################################################
    def __init__(self):
        
        self._FH.setLevel(logging.DEBUG)
        self._FH.setFormatter(self._FDF)
        self._SH.setLevel(logging.WARNING)
        self._SH.setFormatter(self._SDF)
    
################################################################################    
    def _log(self, name: str, level: int, message: str) -> None:

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(self._FH)
        logger.addHandler(self._SH)
        
        logger.log(level, message, exc_info=level >= logging.CRITICAL)
    
################################################################################
    def debug(self, logger_name: str, message: str) -> None:
        
        self._log(logger_name, logging.DEBUG, message)
        
################################################################################
    def info(self, logger_name: str, message: str) -> None:
        
        self._log(logger_name, logging.INFO, message)
        
################################################################################
    def warning(self, logger_name: str, message: str) -> None:
        
        self._log(logger_name, logging.WARNING, message)
        
################################################################################
    def error(self, logger_name: str, message: str) -> None:
        
        self._log(logger_name, logging.ERROR, message)
        
################################################################################
    def critical(self, logger_name: str, message: str) -> None:
        
        self._log(logger_name, logging.CRITICAL, message)
        
################################################################################

log = _FroggeLog()

################################################################################
