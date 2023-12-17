import logging
import sys

import configReader

'''
Author Name: Dileep P B - I530925
Author ID: I530925
Script Usage: Main script for writting logs
'''

# General- Log setting
logFileName = configReader.getLogFileName()
logging.basicConfig(
    handlers=[logging.FileHandler(logFileName, 'w', 'utf-8')],
    level=logging.DEBUG,  # CRITICAL ERROR WARNING  INFO    DEBUG    NOTSET
    datefmt='%Y-%m-%d %H:%M:%S'
)


# format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
def writeLogInfo(severity, content):
    content = sys._getframe(1).f_code.co_filename + '::-' + sys._getframe(1).f_code.co_name + '::-' + str(content)
    if severity == 'Error':
        logging.error(content)
    elif severity == 'Debug':
        logging.debug(content)
    elif severity == 'Warning':
        logging.warn(content)
    else:
        logging.error("Writing log failed because of unknow Severity")
