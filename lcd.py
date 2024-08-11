from __future__ import annotations
import ctypes

from eye import lib


from eye import LCDPrintf as _LCDPrintf
from eye import LCDSetPrintf as _LCDSetPrintf
from eye import LCDClear as _LCDClear
from eye import LCDSetPos as _LCDSetPos

def LCDGetPos():
    row = ctypes.c_int()
    col = ctypes.c_int()

    lib.LCDGetPos(ctypes.pointer(row), ctypes.pointer(col))

    return row.value, col.value

from eye import LCDSetColor as _LCDSetColor
from eye import LCDSetFont as _LCDSetFont
from eye import HELVETICA as _HELVETICA, TIMES as _TIMES, COURIER as _COURIER
from eye import NORMAL as _NORMAL, BOLD as _BOLD, ITALICS as _ITALICS

# `lib.LCDSetFontSize`` (incorrectly) defined in eye.py, and also has no python function
lib.LCDSetFontSize.argtypes = [ctypes.c_int]
def LCDSetFontSize(size):
    """
    Doesn't work with x11 on linux.
    """
    return lib.LCDSetFontSize(size)


from eye import LCDSetMode
lib.LCDSetMode.argtypes = [ctypes.c_int] # incorrectly defined in eye.py

from eye import LCDMenu as _LCDMenu
from eye import LCDMenuI as _LCDMenuI


# `eye.LCDGetSize`` wants pointers, so we might as well directly use `lib.LCDGetSize`
def LCDGetSize():
    width = ctypes.c_int()
    height = ctypes.c_int()

    lib.LCDGetSize(ctypes.pointer(width), ctypes.pointer(height))

    return width.value, height.value


from eye import LCDPixel as _LCDPixel
from eye import LCDGetPixel as _LCDGetPixel
from eye import LCDLine as _LCDLine
from eye import LCDArea as _LCDArea
from eye import LCDCircle as _LCDCircle

from eye import LCDImageSize as _LCDImageSize
from eye import LCDImageStart as _LCDImageStart
from eye import LCDImage, LCDImageGray, LCDImageBinary

from eye import LCDRefresh as _LCDRefresh
