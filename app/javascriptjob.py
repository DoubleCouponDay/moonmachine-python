import os
from settings import DEBUG

def javascriptjob():
    """using grunt because there will be multiple bundles in the future and separate node_modules files.
    """
    os.chdir(os.path.abspath("../node_modules/.bin"))

    if DEBUG:         
        
        os.system("grunt development" + " --gruntfile ../../grunt_webjob.js --verbose")

    else:
        os.system("grunt production" + " --gruntfile ../../grunt_webjob.js --verbose")

    os.chdir(os.path.abspath("../../app"))