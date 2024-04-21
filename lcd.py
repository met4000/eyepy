from __future__ import annotations
import ctypes
from enum import Enum
from typing import Callable, NamedTuple, Optional, TypeVar

try:
    from typing import Final, Literal
except ImportError:
    from typing_extensions import Final, Literal

from eye import lib

from eyepy.drawing import Image, ImageResolution, Colour, IntPoint, IntPointLike, Point, PointLike, colour_to_str, make_coord_map


def _LCD_OK(return_code: int) -> bool:
    """
    Default LCD return code checking behaviour.
    """
    return return_code == 0

from eye import LCDPrintf as _LCDPrintf
def LCDPrintf(format: str, *data: str) -> bool:
    return_code = _LCDPrintf(format, *data)
    return _LCD_OK(return_code)

from eye import LCDSetPrintf as _LCDSetPrintf
def LCDSetPrintf(row: int, col: int, format: str, *data: str) -> bool:
    return_code = _LCDSetPrintf(row, col, format, *data)
    return _LCD_OK(return_code)

from eye import LCDClear as _LCDClear
def LCDClear() -> bool:
    return_code = _LCDClear()
    return _LCD_OK(return_code)

from eye import LCDSetPos as _LCDSetPos
def LCDSetPos(row: int, col: int) -> bool:
    return_code = _LCDSetPos(row, col)
    return _LCD_OK(return_code)

class LCDPos(NamedTuple):
    row: int
    col: int

def LCDGetPos() -> LCDPos:
    """
    Throws a `RuntimeError` if the internal call to `LCDGetPos` returns an error value.
    """
    row = ctypes.c_int()
    col = ctypes.c_int()

    return_code = lib.LCDGetPos(ctypes.pointer(row), ctypes.pointer(col))
    if not _LCD_OK(return_code): raise RuntimeError()

    return LCDPos(row=row.value, col=col.value)

def _validate_colours(*cols: Colour):
    """
    Throws a `ValueError` if a colour is invalid.
    """
    for col in cols:
        if col < 0x000000 or col > 0xFFFFFF:
            raise ValueError(f"colour {colour_to_str(col)} is not a valid colour (out of bounds)")

from eye import LCDSetColor as _LCDSetColor
def LCDSetColor(*, foreground: Colour, background: Colour, validate_cols: bool = True) -> bool:
    """
    :param:`foreground` and :param:`background` use RGB hex colour codes,
    e.g. 0x000000 => black, 0xFFFFFF => white.

    See the docs for the predefined colour constants.
    """
    if validate_cols: _validate_colours(foreground, background)
    return_code = _LCDSetColor(foreground, background)
    return _LCD_OK(return_code)

# can't use unions of pre-defined literals, so we use enums to get type checking
from eye import HELVETICA as _HELVETICA, TIMES as _TIMES, COURIER as _COURIER
class Font(Enum):
    HELVETICA = _HELVETICA
    TIMES = _TIMES
    COURIER = _COURIER
HELVETICA: Final[Font] = Font.HELVETICA
TIMES: Final[Font] = Font.TIMES
COURIER: Final[Font] = Font.COURIER

from eye import NORMAL as _NORMAL, BOLD as _BOLD, ITALICS as _ITALICS
class FontVariation(Enum):
    NORMAL = _NORMAL
    BOLD = _BOLD
    ITALICS = _ITALICS
NORMAL: Final[FontVariation] = FontVariation.NORMAL
BOLD: Final[FontVariation] = FontVariation.BOLD
ITALICS: Final[FontVariation] = FontVariation.ITALICS

from eye import LCDSetFont as _LCDSetFont
def LCDSetFont(font: Font, variation: FontVariation) -> bool:
    """
    Doesn't work with x11 on linux.
    """
    return_code = _LCDSetFont(font, variation)
    return _LCD_OK(return_code)

FontSize = Literal[8, 10, 12, 14, 18, 24]

# `lib.LCDSetFontSize`` (incorrectly) defined in eye.py, and also has no python function
lib.LCDSetFontSize.argtypes = [ctypes.c_int]
def LCDSetFontSize(size: FontSize) -> bool:
    """
    Doesn't work with x11 on linux.
    """
    return_code = lib.LCDSetFontSize(size)
    return _LCD_OK(return_code)

LCDMode = int

from eye import LCDSetMode as _LCDSetMode
lib.LCDSetMode.argtypes = [ctypes.c_int] # incorrectly defined in eye.py
def LCDSetMode(mode: LCDMode) -> bool:
    """
    Appears to do stuff in libeyesim, but hasn't seemed
    to change the LCD behaviour during testing.
    """
    return_code = _LCDSetMode(mode)
    return _LCD_OK(return_code)

from eye import LCDMenu as _LCDMenu
def LCDMenu(str1: str, str2: str, str3: str, str4: str) -> bool:
    return_code = _LCDMenu(str1, str2, str3, str4)
    return _LCD_OK(return_code)

from eye import LCDMenuI as _LCDMenuI
def LCDMenuI(entry: int, string: str, *, foreground: Colour, background: Colour, validate_cols: bool = True) -> bool:
    if validate_cols: _validate_colours(foreground, background)
    return_code = _LCDMenuI(entry, string, foreground, background)
    return _LCD_OK(return_code)

class LCDSize(NamedTuple):
    width: int
    """px"""
    height: int
    """px"""

# `eye.LCDGetSize`` wants pointers, so we might as well directly use `lib.LCDGetSize`
def LCDGetSize() -> LCDSize:
    """
    Throws a `RuntimeError` if the internal call to `LCDGetSize` returns an error value.
    Printable pixel values include 0 but exclude the values returned.
    """
    width = ctypes.c_int()
    height = ctypes.c_int()

    return_code = lib.LCDGetSize(ctypes.pointer(width), ctypes.pointer(height))
    if not _LCD_OK(return_code): raise RuntimeError()

    return LCDSize(width=width.value, height=height.value)

def lcd_make_coord_map(p2: PointLike, *, p1: PointLike = Point(0, 0)) -> Callable[[Point], IntPoint]:
    """
    Produces a function flipping the y axis, mapping :param:`p2` to the
    top right of the screen, and :param:`p1` to the bottom left.
    
    """
    display_max_x, display_max_y = LCDGetSize()

    bottom_left = Point(0, display_max_y - 1)
    top_right = Point(display_max_x - 1, 0)

    f = make_coord_map((p1, p2), (bottom_left, top_right))
    f_int: Callable[[Point], IntPoint] = lambda p: f(p).round()

    return f_int

def lcd_default_point_map(p: Point) -> IntPoint:
    return p.round()

lcd_default_world_coord_map = lcd_make_coord_map((2000, 2000))

_lcd_point_map: Callable[[Point], IntPoint] = lcd_default_point_map

def LCDSetPointMap(f: Callable[[Point], IntPoint]):
    global _lcd_point_map
    _lcd_point_map = f

from eye import LCDPixel as _LCDPixel
def LCDPixel(pixel: PointLike, col: Colour, *, validate_col: bool = True, point_map_override: Callable[[Point], IntPoint] | None = None) -> bool:
    if validate_col: _validate_colours(col)
    pixel = Point(*pixel)
    
    map = _lcd_point_map
    if point_map_override is not None:
        map = point_map_override
    mapped_point = map(pixel)

    return_code = _LCDPixel(mapped_point.x, mapped_point.y, col)
    return _LCD_OK(return_code)

from eye import LCDGetPixel as _LCDGetPixel
def LCDGetPixel(pixel: PointLike, *, validate: bool = True, point_map_override: Callable[[Point], IntPoint] | None = None) -> Colour:
    """
    If :param:`validate` is `True`, a `RuntimeError` will be thrown if
    an invalid colour is returned by `LCDGetPixel`.
    """
    pixel = Point(*pixel)

    map = _lcd_point_map
    if point_map_override is not None:
        map = point_map_override
    mapped_point = map(pixel)

    col = _LCDGetPixel(mapped_point.x, mapped_point.y)

    if validate:
        try:
            _validate_colours(col)
        except ValueError as err:
            raise RuntimeError(*err.args)
    
    return col

from eye import LCDLine as _LCDLine
def LCDLine(p1: PointLike, p2: PointLike, col: Colour, *, validate_col: bool = True, point_map_override: Callable[[Point], IntPoint] | None = None) -> bool:
    if validate_col: _validate_colours(col)
    p1 = Point(*p1)
    p2 = Point(*p2)

    map = _lcd_point_map
    if point_map_override is not None:
        map = point_map_override
    mapped_p1 = map(p1)
    mapped_p2 = map(p2)

    return_code = _LCDLine(mapped_p1.x, mapped_p1.y, mapped_p2.x, mapped_p2.y, col)
    return _LCD_OK(return_code)

from eye import LCDArea as _LCDArea
def LCDArea(p1: PointLike, p2: PointLike, col: Colour, *, fill: bool = True, validate_col: bool = True, point_map_override: Callable[[Point], IntPoint] | None = None) -> bool:
    if validate_col: _validate_colours(col)
    p1 = Point(*p1)
    p2 = Point(*p2)

    map = _lcd_point_map
    if point_map_override is not None:
        map = point_map_override
    mapped_p1 = map(p1)
    mapped_p2 = map(p2)

    return_code = _LCDArea(mapped_p1.x, mapped_p1.y, mapped_p2.x, mapped_p2.y, col, int(fill))
    return _LCD_OK(return_code)

from eye import LCDCircle as _LCDCircle
def LCDCircle(centre: PointLike, size: int, col: Colour, *, fill: bool = True, validate_col: bool = True, point_map_override: Callable[[Point], IntPoint] | None = None) -> bool:
    """
    TODO check what 'size' means (radius? diameter?)

    Note: size is not scaled by the point map
    """
    if validate_col: _validate_colours(col)
    centre = Point(*centre)

    map = _lcd_point_map
    if point_map_override is not None:
        map = point_map_override
    mapped_centre = map(centre)

    return_code = _LCDCircle(mapped_centre.x, mapped_centre.y, size, col, int(fill))
    return _LCD_OK(return_code)

_image_position: IntPoint = IntPoint(0, 0)

from eye import LCDImageSize as _LCDImageSize
def LCDImageSize(resolution: ImageResolution) -> bool:
    """
    Note: the image size is automatically set when printed by
    :func:`LCDImage`, :func:`LCDImageGray`, or :func:`LCDImageBinary`;
    this function does not need to be called manually.
    """
    resolution_code = resolution._code
    return_code = _LCDImageSize(resolution_code)
    return _LCD_OK(return_code)

from eye import LCDImageStart as _LCDImageStart
def LCDImageStart(start: IntPointLike, *, width: int, height: int) -> bool:
    """
    Sets default image position and size.

    Note: image size will be overwritten automatically when calls to :func:`LCDImage`,
    :func:`LCDImageGray`, or :func:`LCDImageBinary` are made.
    """
    start = IntPoint(*start)
    return_code = _LCDImageStart(start.x, start.y, width, height)
    if not _LCD_OK(return_code):
        return False
    
    global _image_position
    _image_position = start
    return True

R = TypeVar("R")
def _lcd_image_print_base(image: Image, *, print_func: Callable[[ctypes.Array[ctypes.c_byte]], R], ok_predicate: Callable[[R], bool], start: Optional[IntPointLike]) -> bool:
    default_position = _image_position
    if not LCDImageStart(
        start if start is not None else default_position,
        width=image.resolution.WIDTH,
        height=image.resolution.HEIGHT
    ): return False

    image_bytes = image._c_bytes
    return_code = print_func(image_bytes)

    if start is not None:
        if not LCDImageStart(default_position, width=image.resolution.WIDTH, height=image.resolution.HEIGHT):
            return False

    return ok_predicate(return_code)

# `eye.LCDImage` simply wraps it, so we directly use `lib.LCDImage`
def LCDImage(image: Image, *, start: Optional[IntPointLike] = None) -> bool:
    """
    Returns `False` if the image is not the correct type (e.g. is a gray image),
    or if the internal calls to `LCDImageStart` or `LCDImage` return an error value.

    If :param:`start` is specified, it will be used for the image position rather
    than the current default image position. Does not override the default image position.
    """
    if image.is_gray:
        return False
    
    return _lcd_image_print_base(image, print_func=lib.LCDImage, ok_predicate=_LCD_OK, start=start)

# `eye.LCDImageGray` simply wraps it, so we directly use `lib.LCDImageGray`
def LCDImageGray(image: Image, *, start: Optional[IntPointLike] = None) -> bool:
    """
    Returns `False` if the image is not the correct type (e.g. is a colour image),
    or if the internal calls to `LCDImageStart` or `LCDImageGray` return an error value.

    If :param:`start` is specified, it will be used for the image position rather
    than the current default image position. Does not override the default image position.
    """
    if not image.is_gray:
        return False
    
    return _lcd_image_print_base(image, print_func=lib.LCDImageGray, ok_predicate=_LCD_OK, start=start)

# `eye.LCDImageBinary` simply wraps it, so we directly use `lib.LCDImageBinary`
def LCDImageBinary(image: Image, *, start: Optional[IntPointLike] = None) -> bool:
    """
    Expects a gray image using only 0 (white) and 1 (black).
    If :param:`validate` is `True`, will return `False` if the image is not
    the correct type (e.g. is not binary). If :param:`validate` is `False`,
    no attempt to validate the image will be made.

    If :param:`start` is specified, it will be used for the image position rather
    than the current default image position. Does not override the default image position.

    Note: appears to be :func:`LCDImageGray`, but subtracting 1 from each pixel
    (with 0 - 1 => 255 (white), 1 - 1 => 0 (black), and every other value
    remaining approximately the same).
    """
    if not image.is_gray:
        return False
    
    return _lcd_image_print_base(image, print_func=lib.LCDImageBinary, ok_predicate=_LCD_OK, start=start)

from eye import LCDRefresh as _LCDRefresh
def LCDRefresh() -> bool:
    return_code = _LCDRefresh()
    return _LCD_OK(return_code)

# TODO LCD modes?
