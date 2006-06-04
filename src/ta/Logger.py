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
logger_handlers = [(logging.StreamHandler(), logging.INFO), 
           (logging.handlers.TimedRotatingFileHandler(filename='ta.log', when='midnight', backupCount=10), logging.DEBUG)]
    
def logger(name='ta', level=logger_level, format=logger_format,
           date_format=logger_date_format):
    """ logger(level) -> returns a logger all fixed up
        add handlers if needed in the logger_handlers list
    
    """
    logger = logging.getLogger(name)
    formatter = logging.Formatter(format, date_format)
    for handler, handler_level in logger_handlers:
        handler.setLevel(handler_level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
    

