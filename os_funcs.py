import ctypes
import datetime
import time
from typing import Callable, Literal, NamedTuple

from eye import lib


# SYSTEM

# TODO figure out what the format is - passing a string caused a segfault
from eye import OSExecute

def OSVersion() -> str:
    """
    Unable to get a non-error value during testing when run in sim.
    """
    raise NotImplementedError()

def OSVersionIO() -> str:
    """
    Unable to get a non-error value during testing when run in sim.
    """
    raise NotImplementedError()

from eye import OSMachineSpeed as _OSMachineSpeed
def OSMachineSpeed() -> int:
    return _OSMachineSpeed()

from eye import OSMachineType as _OSMachineType
def OSMachineType() -> int:
    """
    Seems to be hardcoded to return 1 in the source code on linux,
    and also returns 1 on windows (even when a robot is not present).
    """
    return _OSMachineType()

def OSMachineName() -> str:
    """
    Unable to get a non-error value during testing when run in sim.
    """
    raise NotImplementedError()

from eye import OSMachineID as _OSMachineID
def OSMachineID() -> int:
    return _OSMachineID()


# TIMER

def _TIMER_OK(return_code: int) -> bool:
    """
    Default timer return code checking behaviour.
    """
    return return_code == 0

def OSWait(ms: int) -> bool:
    # Note: eyesim's `OSWait` seems to use `usleep`, which stops
    # working after the core timer has been initialised, so this
    # has an alternate implementation using `time.sleep`
    time.sleep(ms / 1000)
    return True

Timer = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17] # from testing, the timer count does not seem to be able to exceed 17

from eye import OSAttachTimer as _OSAttachTimer
def OSAttachTimer(period_ms: int, f: Callable[[], None]) -> Timer:
    """
    ! Unstable behaviour when tested in sim. While timers were running, other python operations could lead to segfaults.
    """
    return _OSAttachTimer(period_ms, f)

from eye import OSDetachTimer as _OSDetachTimer
def OSDetachTimer(timer: Timer) -> bool:
    return_code = _OSDetachTimer(timer)
    return _TIMER_OK(return_code)

class OSTime(NamedTuple):
    hours: int
    mins: int
    secs: int
    ms: int

lib.OSGetTime.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
def OSGetTime() -> OSTime:
    """
    Appears to return the system's time (in GMT) in sim.
    Throws a `RuntimeError` if the internal call to `OSGetTime` returns an error value.
    See :func:`OSGetTimePy` for a version of this function that outputs a :class:`datetime.time`.
    """
    hours = ctypes.c_int()
    mins = ctypes.c_int()
    secs = ctypes.c_int()
    ms = ctypes.c_int()
    
    return_code: int = lib.OSGetTime(ctypes.pointer(hours), ctypes.pointer(mins), ctypes.pointer(secs), ctypes.pointer(ms))
    if return_code != 0: raise RuntimeError()
    
    return OSTime(hours=hours.value, mins=mins.value, secs=secs.value, ms=ms.value)

def OSGetTimePy() -> datetime.time:
    """
    Calls :func:`OSGetTime` and then converts the output to a python :class:`datetime.time`.
    Throws a `RuntimeError` if the internal call to `OSGetTime` returns an error value.
    """
    hours, mins, secs, ms = OSGetTime()
    return datetime.time(hour=hours, minute=mins, second=secs, microsecond=ms*1000)


# It seems like OSGetCount requires a call to `TIMInitialise_core_timer` before
# it will start counting. `OSAttachTimer` calls this, so we attach and then detach
# a dummy function to initialise the timer (approximately) as the program starts
OSDetachTimer(OSAttachTimer(1000, type(None)))

from eye import OSGetCount as _OSGetCount
def OSGetCount() -> int:
    """
    Returns ms since system start.
    In sim, the system start is approximately when the python program is started.
    """
    return _OSGetCount()
