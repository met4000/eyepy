import ctypes
from enum import Enum
from typing import Optional

from eye import lib


# use `None` in place of NOKEY and ANYKEY
from eye import NOKEY as _NOKEY, ANYKEY as _ANYKEY

# can't use unions of pre-defined literals, so we use enums to get type checking
from eye import KEY1 as _KEY1, KEY2 as _KEY2, KEY3 as _KEY3, KEY4 as _KEY4

from eyepy.drawing import Point
class Key(Enum):
    KEY1 = _KEY1
    KEY2 = _KEY2
    KEY3 = _KEY3
    KEY4 = _KEY4
KEY1 = Key.KEY1
KEY2 = Key.KEY2
KEY3 = Key.KEY3
KEY4 = Key.KEY4

from eye import KEYGet as _KEYGet
def KEYGet() -> Key:
    """
    Blocking read for key press.
    """
    key: int = _KEYGet()
    cast_key = Key(key)
    return cast_key

from eye import KEYRead as _KEYRead
def KEYRead() -> Key | None:
    """
    Non-blocking read of key press (returns `None` if no key is pressed).
    """
    key: int = _KEYRead()

    if key == _NOKEY:
        return None
    
    cast_key = Key(key)
    return cast_key

from eye import KEYWait as _KEYWait
def KEYWait(key: Optional[Key] = None) -> Key:
    """
    Blocking read until the specified key (or any key if `None`) has been pressed.
    Returns the key that was pressed.
    """
    raw_key = _ANYKEY if key is None else key.value
    found_key = _KEYWait(raw_key)
    cast_key = Key(found_key)
    return cast_key

# `eye.KEYGetXY`` wants pointers, so we might as well directly use `lib.KEYGetXY`
def KEYGetXY() -> Point:
    """
    Blocking read for a touch at any position.
    Throws a `RuntimeError` if the internal call to `KEYGetXY` returns an error value.
    Returns the coordinates of the touch.
    """
    x = ctypes.c_int()
    y = ctypes.c_int()

    return_code = lib.KEYGetXY(ctypes.pointer(x), ctypes.pointer(y))
    if return_code != 0: raise RuntimeError()

    return Point(x=x.value, y=y.value)

# `eye.KEYReadXY`` wants pointers, so we might as well directly use `lib.KEYReadXY`
def KEYReadXY() -> Point | None:
    """
    Non-blocking read for a touch at any position.
    Throws a `RuntimeError` if the internal call to `KEYReadXY` returns an error value.
    Returns the coordinates of the touch, or `None`.
    """
    x = ctypes.c_int()
    y = ctypes.c_int()

    return_code = lib.KEYReadXY(ctypes.pointer(x), ctypes.pointer(y))
    if return_code == 1:
        # no touch
        return None
    
    if return_code != 0:
        raise RuntimeError()

    return Point(x=x.value, y=y.value)
