import ctypes


from eye import lib



from eye import NOKEY, ANYKEY
from eye import KEY1 as _KEY1, KEY2 as _KEY2, KEY3 as _KEY3, KEY4 as _KEY4

from eye import KEYGet as _KEYGet
from eye import KEYRead as _KEYRead
from eye import KEYWait as _KEYWait


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
