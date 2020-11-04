#!/usr/bin/env python3
# PYTHON_PREAMBLE_START_STANDARD:{{{

# Christopher David Cotton (c)
# http://www.cdcotton.com

# modules needed for preamble
import importlib
import os
from pathlib import Path
import sys

# Get full real filename
__fullrealfile__ = os.path.abspath(__file__)

# Function to get git directory containing this file
def getprojectdir(filename):
    curlevel = filename
    while curlevel is not '/':
        curlevel = os.path.dirname(curlevel)
        if os.path.exists(curlevel + '/.git/'):
            return(curlevel + '/')
    return(None)

# Directory of project
__projectdir__ = Path(getprojectdir(__fullrealfile__))

# Function to call functions from files by their absolute path.
# Imports modules if they've not already been imported
# First argument is filename, second is function name, third is dictionary containing loaded modules.
modulesdict = {}
def importattr(modulefilename, func, modulesdict = modulesdict):
    # get modulefilename as string to prevent problems in <= python3.5 with pathlib -> os
    modulefilename = str(modulefilename)
    # if function in this file
    if modulefilename == __fullrealfile__:
        return(eval(func))
    else:
        # add file to moduledict if not there already
        if modulefilename not in modulesdict:
            # check filename exists
            if not os.path.isfile(modulefilename):
                raise Exception('Module not exists: ' + modulefilename + '. Function: ' + func + '. Filename called from: ' + __fullrealfile__ + '.')
            # add directory to path
            sys.path.append(os.path.dirname(modulefilename))
            # actually add module to moduledict
            modulesdict[modulefilename] = importlib.import_module(''.join(os.path.basename(modulefilename).split('.')[: -1]))

        # get the actual function from the file and return it
        return(getattr(modulesdict[modulefilename], func))

# PYTHON_PREAMBLE_END:}}}

def truefalsedo(truefalseval, dofunc, secondintervals, tempfolder):
    """
    This is a very simple function which is designed as a wrapper for calling another function, dofunc, only when truefalseval is False for more seconds than an element in secondintervals. It only calls the function once.

    Arguments:
    If False for more than secondintervals, run dofunc once.
    dofunc takes single argument, seconds (integer).
    tempfolder is where I save necessary files detailing what has happened in past.

    Example:
    I use this function for calling popups e.g. if I want to call if something has been broken for a while. Then I write a function which determines whether the item is broken (if it is truefalseval is False otherwise True) and then I call this function with the popup function as dofunc.
    """
    import datetime
    import os
    import shutil

    try:
        os.mkdir(tempfolder)
    except FileExistsError:
        None

    dateformat = "%y%m%d_%H%M%S"

    # get seconds since last True. Set to zero secs if no record.
    lastrun = None
    if os.path.isfile(os.path.join(tempfolder, 'date.txt')):
        with open(os.path.join(tempfolder, 'date.txt')) as f:
             lastrun = f.read()
             lastrun = datetime.datetime.strptime(lastrun, dateformat)

        secssincelastrun = (datetime.datetime.now() -  lastrun).seconds
    else:
        secssincelastrun = 0

    if truefalseval is True:
        with open(os.path.join(tempfolder, 'date.txt'), 'w+') as f:
            f.write(datetime.datetime.now().strftime(dateformat))

        try:
            shutil.rmtree(os.path.join(tempfolder, 'seconds'))
        except FileNotFoundError:
            None
    else:
        try:
            os.mkdir(os.path.join(tempfolder, 'seconds'))
        except FileExistsError:
            None

        for second in secondintervals:
            if second <= secssincelastrun:
                if not os.path.isfile(os.path.join(tempfolder, 'seconds', str(second))):
                    dofunc(lastrun)
                    
                    with open(os.path.join(tempfolder, 'seconds', str(second)), 'w+') as f:
                        f.write('')
                    
