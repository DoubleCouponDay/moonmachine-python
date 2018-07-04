import os
from settings import DEBUG
from logging import getLogger

def javascriptjob():
    """using grunt because there will be multiple bundles in the future and separate node_modules files.
    """    
    logger = getLogger("javascriptjob")
    commonparams = " --gruntfile ../../grunt/grunt_webjob.js --verbose"

    if DEBUG:         
        os.chdir(os.path.abspath("../node_modules/.bin"))    #in development I dont need to do this, but its nice having a shared commonparams
        os.system("grunt development" + commonparams)
        os.chdir(os.path.abspath("../../app"))  

    else:
        gruntpath = os.path.abspath("./node_modules/.bin")
        logger.info("attempting grunt dir: " + gruntpath)
        os.chdir(gruntpath)
        os.system("grunt production" + commonparams)
        returnpath = "../../app"
        logger.info("attempting return dir: " + returnpath)
        os.chdir(returnpath)
    