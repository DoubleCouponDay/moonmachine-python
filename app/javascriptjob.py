import os
from settings import DEBUG

def javascriptjob():
    """using grunt because there will be multiple bundles in the future and separate node_modules files.
    """
    
    if DEBUG:         
        os.system("grunt development" + " --gruntfile ../grunt/grunt_webjob.js --verbose")

    else:
        os.system("grunt production" + " --gruntfile ../grunt/grunt_webjob.js --verbose")