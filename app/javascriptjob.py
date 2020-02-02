import os
from settings import DEBUG
from logging import getLogger
import sys

def javascriptjob():
    """using grunt because there will be multiple bundles in the future and separate node_modules files.
    """    
    logger = getLogger("javascriptjob")
    commonparams = " --gruntfile ../grunt/grunt_webjob.js --verbose"

    if DEBUG:    
        os.system("grunt development" + commonparams)

    else:
        os.system("grunt production" + commonparams)
    