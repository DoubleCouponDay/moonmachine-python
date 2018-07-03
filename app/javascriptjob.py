import os
from settings import DEBUG
from logging import getLogger

def javascriptjob():
    """using grunt because there will be multiple bundles in the future and separate node_modules files.
    """    
    logger = getLogger("javascriptjob")

    if DEBUG:         
        os.chdir(os.path.abspath("../node_modules/.bin"))    
        os.system("grunt development" + " --gruntfile ../../grunt_webjob.js --verbose")
        os.chdir(os.path.abspath("../../app"))  

    else:
        gruntpath = os.path.abspath("./node_modules/.bin")
        logger.info("attempting gruntpath: " + gruntpath)
        os.chdir(gruntpath)
        os.system("grunt production" + " --gruntfile ../../grunt_webjob.js --verbose")
        returnpath = "../../app"
        logger.info("attempting returnpath: " + returnpath)
        os.chdir(returnpath)
    