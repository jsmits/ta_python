#!/usr/bin/env python
""" ta.Logger -> Logging module for use elsewhere in this package.

"""
import logging
import logging.handlers
import os
import sys

logger_format = '%(asctime)s  %(levelname)-9.9s %(message)s  %(module)s.py:%(lineno)d'
logger_date_format = '%d-%m-%Y %H:%M:%S'
logger_level = int(os.environ.get('TA_LOGLEVEL', logging.INFO))
logger_level_debug = int(os.environ.get('TA_DEBUG_LOGLEVEL', logging.DEBUG))
logger_handlers = [(logging.StreamHandler(), logger_level), 
           (logging.handlers.RotatingFileHandler(filename='ta.log', maxBytes=10*1024*1024, backupCount=10), logger_level_debug)]
    
def logger(name='ta', level=logger_level_debug, format=logger_format,
           date_format=logger_date_format):
    """ logger(level) -> returns a logger all fixed up
        add handlers if needed in the logger_handlers list
    
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter(format, date_format)
    for handler, handler_level in logger_handlers:
        handler.setLevel(handler_level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
    

