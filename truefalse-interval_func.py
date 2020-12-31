#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

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
                    
