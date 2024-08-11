"""Wrapper around `eye` module, fixing bugs and other problems."""

import ctypes
import time

from eye import lib



# ------------------------------ LCD ------------------------------

from eye import LCDPrintf
from eye import LCDSetPrintf
from eye import LCDClear
from eye import LCDSetPos

def LCDGetPos():
    row = ctypes.c_int()
    col = ctypes.c_int()

    lib.LCDGetPos(ctypes.pointer(row), ctypes.pointer(col))

    return row.value, col.value

from eye import LCDSetColor
from eye import LCDSetFont
from eye import HELVETICA, TIMES, COURIER
from eye import NORMAL, BOLD, ITALICS

# `lib.LCDSetFontSize`` (incorrectly) defined in eye.py, and also has no python function
lib.LCDSetFontSize.argtypes = [ctypes.c_int]
def LCDSetFontSize(size):
    """
    Doesn't work with x11 on linux.
    """
    return lib.LCDSetFontSize(size)


from eye import LCDSetMode
lib.LCDSetMode.argtypes = [ctypes.c_int] # incorrectly defined in eye.py

from eye import LCDMenu
from eye import LCDMenuI


# `eye.LCDGetSize`` wants pointers, so we might as well directly use `lib.LCDGetSize`
def LCDGetSize():
    width = ctypes.c_int()
    height = ctypes.c_int()

    lib.LCDGetSize(ctypes.pointer(width), ctypes.pointer(height))

    return width.value, height.value


from eye import LCDPixel
from eye import LCDGetPixel
from eye import LCDLine
from eye import LCDArea
from eye import LCDCircle

from eye import LCDImageSize
from eye import LCDImageStart
from eye import LCDImage
from eye import LCDImageGray
from eye import LCDImageBinary

from eye import LCDRefresh



# ------------------------------ KEYS ------------------------------

from eye import NOKEY, ANYKEY
from eye import KEY1, KEY2, KEY3, KEY4

from eye import KEYGet
from eye import KEYRead
from eye import KEYWait


# `eye.KEYGetXY`` wants pointers, so we might as well directly use `lib.KEYGetXY`
def KEYGetXY():
    x = ctypes.c_int()
    y = ctypes.c_int()

    lib.KEYGetXY(ctypes.pointer(x), ctypes.pointer(y))

    return x.value, y.value

# `eye.KEYReadXY`` wants pointers, so we might as well directly use `lib.KEYReadXY`
def KEYReadXY():
    x = ctypes.c_int()
    y = ctypes.c_int()

    return_code = lib.KEYReadXY(ctypes.pointer(x), ctypes.pointer(y))
    if return_code == 1:
        # no touch
        return NOKEY

    return x.value, y.value



# ------------------------------ CAMERA ------------------------------

from eye import RED, GREEN, BLUE, WHITE, GRAY, BLACK, ORANGE, SILVER, LIGHTGRAY, DARKGRAY, NAVY, CYAN, TEAL, MAGENTA, PURPLE, MAROON, YELLOW, OLIVE

from eye import QQVGA, QQVGA_X, QQVGA_Y
from eye import QVGA, QVGA_X, QVGA_Y
from eye import VGA, VGA_X, VGA_Y
from eye import CAM1MP, CAM1MP_X, CAM1MP_Y
from eye import CAMHD, CAMHD_X, CAMHD_Y
from eye import CAM5MP, CAM5MP_X, CAM5MP_Y
from eye import CUSTOM

from eye import CAMInit
from eye import CAMRelease

from eye import CAMGet
from eye import CAMGetGray



# ------------------------------ IMAGE PROCESSING ------------------------------

# untested
from eye import IPSetSize
from eye import IPReadFile
from eye import IPWriteFile
from eye import IPWriteFileGray

# untested
from eye import IPLaplace
from eye import IPSobel
from eye import IPCol2Gray
from eye import IPGray2Col
from eye import IPRGB2Col
from eye import IPCol2HSI
from eye import IPOverlay
from eye import IPOverlayGray


from eye import IPPRGB2Col
from eye import IPPCol2RGB

from eye import IPPCol2HSI as _IPPCol2HSI
def IPPCol2HSI(col):
    h = ctypes.c_int()
    s = ctypes.c_int()
    i = ctypes.c_int()

    _IPPCol2HSI(col, ctypes.pointer(h), ctypes.pointer(s), ctypes.pointer(i))
    
    return h.value, s.value, i.value

from eye import IPPRGB2Hue
from eye import IPPRGB2HSI



# ------------------------------ OS FUNCS ------------------------------

# ---------- SYSTEM ----------

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


# ---------- TIMER ----------

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



# ------------------------------ USB/SERIAL ------------------------------

# untested
from eye import SERInit
from eye import SERSendChar
from eye import SERSend
from eye import SERReceiveChar
from eye import SERReceive
from eye import SERFlush
from eye import SERClose



# ------------------------------ AUDIO ------------------------------

# untested
from eye import AUBeep
from eye import AUPlay
from eye import AUDone
from eye import AUMicrophone



# ------------------------------ DISTANCE SENSORS ------------------------------


# ---------- PSD ----------

from eye import PSD_FRONT, PSD_LEFT, PSD_RIGHT, PSD_BACK

from eye import PSDGet
from eye import PSDGetRaw


# ---------- LIDAR ----------

from eye import LIDARGet
from eye import LIDARSet



# ------------------------------ SERVOS/MOTORS ------------------------------

# ---------- SERVOS ----------

from eye import SERVOSet
from eye import SERVOSetRaw
from eye import SERVORange

# ---------- MOTORS ----------

from eye import MOTORDrive
from eye import MOTORDriveRaw
from eye import MOTORPID
from eye import MOTORPIDOff
from eye import MOTORSpeed

# ---------- ENCODERS ----------

from eye import ENCODERRead
from eye import ENCODERReset



# ------------------------------ V-OMEGA ------------------------------

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



# ------------------------------ I/O ------------------------------

# ---------- DIGITAL ----------

# untested
from eye import DIGITALSetup
from eye import DIGITALRead
from eye import DIGITALReadAll
from eye import DIGITALWrite

# ---------- ANALOG ----------

# untested
from eye import ANALOGRead
from eye import ANALOGVoltage
from eye import ANALOGRecord
from eye import ANALOGTransfer



# ------------------------------ IR REMOTE CONTROL ------------------------------

# TODO ir


# ------------------------------ RADIO COMS ------------------------------

# TODO radio communication



# ------------------------------ SIM ONLY ------------------------------

from eye import SIMGetRobot
from eye import SIMSetRobot
from eye import SIMGetObject
from eye import SIMSetObject

# TODO
# from eye import SIMGetRobotCount
# from eye import SIMGetObjectCount
