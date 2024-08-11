import ctypes

from eye import lib


from eye import VWSetSpeed

# `lib.VWGetSpeed`` (incorrectly) defined in eye.py, and also has no python function
lib.VWGetSpeed.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
def VWGetSpeed() -> tuple[int, int]:
    """
    Note: from testing the returned values seem to be measured, rather than getting
    the values currently trying to be achieved by e.g. :func:`VWSetSpeed`.
    """
    lin_speed = ctypes.c_int()
    ang_speed = ctypes.c_int()

    lib.VWGetSpeed(ctypes.pointer(lin_speed), ctypes.pointer(ang_speed))

    return lin_speed.value, ang_speed.value


from eye import VWSetPosition
from eye import VWGetPosition
from eye import VWStraight
from eye import VWTurn
from eye import VWCurve
from eye import VWDrive

from eye import VWRemain
from eye import VWDone
from eye import VWWait
from eye import VWStalled
