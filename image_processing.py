import ctypes


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
