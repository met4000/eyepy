from __future__ import annotations
from collections.abc import Sequence
import ctypes
import itertools
from typing import Final, Literal, NamedTuple, cast, overload


class Point(NamedTuple):
    x: int
    y: int


from eye import CUSTOM as _CUSTOM
class ImageResolution:
    WIDTH: Final[int]
    HEIGHT: Final[int]
    PIXELS: Final[int]
    SIZE: Final[int]
    _code: Final[int]

    def __init__(self, width: int, height: int, _code: int = _CUSTOM):
        """
        :param:`_code` should not be used.
        """
        self.WIDTH = width
        self.HEIGHT = height
        self.PIXELS = self.WIDTH * self.HEIGHT
        self.SIZE = self.PIXELS * 3
        self._code = _code

from eye import QQVGA as _QQVGA, QQVGA_X as _QQVGA_X, QQVGA_Y as _QQVGA_Y
QQVGA: Final[ImageResolution] = ImageResolution(_QQVGA_X, _QQVGA_Y, _QQVGA)
from eye import QVGA as _QVGA, QVGA_X as _QVGA_X, QVGA_Y as _QVGA_Y
QVGA: Final[ImageResolution] = ImageResolution(_QVGA_X, _QVGA_Y, _QVGA)
from eye import VGA as _VGA, VGA_X as _VGA_X, VGA_Y as _VGA_Y
VGA: Final[ImageResolution] = ImageResolution(_VGA_X, _VGA_Y, _VGA)
from eye import CAM1MP as _CAM1MP, CAM1MP_X as _CAM1MP_X, CAM1MP_Y as _CAM1MP_Y
CAM1MP: Final[ImageResolution] = ImageResolution(_CAM1MP_X, _CAM1MP_Y, _CAM1MP)
from eye import CAMHD as _CAMHD, CAMHD_X as _CAMHD_X, CAMHD_Y as _CAMHD_Y
CAMHD: Final[ImageResolution] = ImageResolution(_CAMHD_X, _CAMHD_Y, _CAMHD)
from eye import CAM5MP as _CAM5MP, CAM5MP_X as _CAM5MP_X, CAM5MP_Y as _CAM5MP_Y
CAM5MP: Final[ImageResolution] = ImageResolution(_CAM5MP_X, _CAM5MP_Y, _CAM5MP)

class Image(Sequence):
    _c_bytes: ctypes.Array[ctypes.c_byte]
    is_gray: Final[bool]
    resolution: Final[ImageResolution]

    def __init__(self, c_bytes: ctypes.Array[ctypes.c_byte], *, gray: bool = False, resolution: ImageResolution):
        self._c_bytes = c_bytes
        self.is_gray = gray
        self.resolution = resolution

    @staticmethod
    def from_c_bytes(image: ctypes.Array[ctypes.c_byte], *, gray: bool = False, resolution: ImageResolution) -> Image:
        return Image(image, gray=gray, resolution=resolution)
    
    @overload
    @staticmethod
    def from_list(image: list[tuple[int, int, int]], *, gray: Literal[False] = False, resolution: ImageResolution) -> Image: ...

    @overload
    @staticmethod
    def from_list(image: list[int], *, gray: Literal[True], resolution: ImageResolution) -> Image: ...

    @staticmethod
    def from_list(image: list[tuple[int, int, int]] | list[int], *, gray: bool = False, resolution: ImageResolution) -> Image:
        flat_image: list[int]
        if not gray:
            image = cast(list[tuple[int, int, int]], image)
            flat_image = list(itertools.chain.from_iterable(image))
        else:
            flat_image = cast(list[int], image)
        c_bytes = (ctypes.c_byte * len(flat_image))(*flat_image)
        return Image(c_bytes, gray=gray, resolution=resolution)
    
    @overload
    def __getitem__(self, __key: int) -> int: ...
    @overload
    def __getitem__(self, __key: slice) -> list[int]: ...
    def __getitem__(self, *args):
        return self._c_bytes.__getitem__(*args)
    
    def __len__(self) -> int:
        return self._c_bytes.__len__()
