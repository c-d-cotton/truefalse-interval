#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

def test():
    """
    Add file temp/file.txt to return True. Otherwise return False and print error message if new 10 seconds for 1 minutes.
    """
    if os.path.isfile(__projectdir__ / Path('temp/file.txt')):
        truefalseval = True
    else:
        truefalseval = False

    def dofunc(date):
        print(date)

    from truefalse_interval_func import truefalsedo
    truefalsedo(truefalseval, dofunc, [10, 20, 30, 40, 50, 60], __projectdir__ / Path('temp/tempfolder/'))

# Run:{{{1
test()
