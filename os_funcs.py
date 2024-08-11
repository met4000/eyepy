from __future__ import annotations
import ctypes
import datetime
import time
from typing import Callable, NamedTuple

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from eye import lib


# SYSTEM

# * not sure what the format is - passing a string caused a segfault
from eye import OSExecute

# * unable to get a non-error value during testing when run in sim for the following funcs
from eye import OSVersion
from eye import OSVersionIO
from eye import OSMachineName

from eye import OSMachineSpeed

# seems to be hardcoded to return 1 in the source code on linux, and also returns 1 on windows (even when a robot is not present).
from eye import OSMachineType

from eye import OSMachineID


# TIMER


def OSWait(ms):
    # Note: eyesim's `OSWait` seems to use `usleep`, which stops
    # working after the core timer has been initialised, so this
    # has an alternate implementation using `time.sleep`
    time.sleep(ms / 1000)
    return 0

# ! Unstable behaviour when tested in sim. While timers were running, other python operations could lead to segfaults.
from eye import OSAttachTimer

from eye import OSDetachTimer

lib.OSGetTime.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
def OSGetTime():
    """
    Appears to return the system's time (in GMT) in sim.
    """
    hours = ctypes.c_int()
    mins = ctypes.c_int()
    secs = ctypes.c_int()
    ms = ctypes.c_int()
    
    lib.OSGetTime(ctypes.pointer(hours), ctypes.pointer(mins), ctypes.pointer(secs), ctypes.pointer(ms))
    
    return hours.value, mins.value, secs.value, ms.value


# It seems like OSGetCount requires a call to `TIMInitialise_core_timer` before
# it will start counting. `OSAttachTimer` calls this, so we attach and then detach
# a dummy function to initialise the timer (approximately) as the program starts
OSDetachTimer(OSAttachTimer(1000, type(None)))

# 'system start' appears to be when the python program is started
from eye import OSGetCount
