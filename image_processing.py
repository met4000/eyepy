from __future__ import annotations
import ctypes

from eyepy.drawing import Colour, colour_to_rgb


from eye import IPPRGB2Col as _IPPRGB2Col

from eyepy.utils import deg_to_rad
def IPPRGB2Col(rgb: tuple[int, int, int]) -> Colour:
    r, g, b = rgb
    return _IPPRGB2Col(r, g, b)

def IPPCol2RGB(col: Colour) -> tuple[int, int, int]:
    return colour_to_rgb(col)

from eye import IPPCol2HSI as _IPPCol2HSI
def IPPCol2HSI(col: Colour) -> tuple[int, int, int]:
    h = ctypes.c_int()
    s = ctypes.c_int()
    i = ctypes.c_int()

    _IPPCol2HSI(col, ctypes.pointer(h), ctypes.pointer(s), ctypes.pointer(i))
    return (h.value, s.value, i.value)

from eye import IPPRGB2Hue as _IPPRGB2Hue
def IPPRGB2Hue(rgb: tuple[int, int, int]) -> int:
    r, g, b = rgb
    return _IPPRGB2Hue(r, g, b)

from eye import IPPRGB2HSI as _IPPRGB2HSI
def IPPRGB2HSI(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    r, g, b = rgb
    h, s, i = _IPPRGB2HSI(r, g, b)
    return (h, s, i)

def IPPHSI2RGB(hsi: tuple[int, int, int]) -> tuple[int, int, int]:
    """
    Expects 0 <= h < 360, 0 <= s <= 255, 0 <= i <= 255.
    """
    h, s, i = hsi

    # uses the algorithm described at https://en.wikipedia.org/wiki/HSL_and_HSV#HSI_to_RGB

    if not (0 <= h < 360): raise ValueError(f"Hue out of range; expected 0 <= h < 360 but got '{h}'")
    h_prime = h / 60

    s /= 255
    i /= 255

    z = 1 - abs(h_prime % 2 - 1)
    c = 3 * i * s / (1 + z)
    x = c * z
    m = i * (1 - s)

    r: float
    g: float
    b: float
    if 0 <= h_prime < 1:
        r, g, b = (c, x, 0)
    elif 1 <= h_prime < 2:
        r, g, b = (x, c, 0)
    elif 2 <= h_prime < 3:
        r, g, b = (0, c, x)
    elif 3 <= h_prime < 4:
        r, g, b = (0, x, c)
    elif 4 <= h_prime < 5:
        r, g, b = (x, 0, c)
    elif 5 <= h_prime < 6:
        r, g, b = (c, 0, x)

    r += m
    g += m
    b += m

    max_rgb = max(r, g, b)
    if max_rgb > 1:
        r /= max_rgb
        g /= max_rgb
        b /= max_rgb
    
    r *= 255
    g *= 255
    b *= 255
    
    return round(r), round(g), round(b)
