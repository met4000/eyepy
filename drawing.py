from __future__ import annotations
from collections.abc import Sequence
import ctypes
import itertools
import math
from typing import Callable, NamedTuple, cast, overload

try:
    from typing import Final, Literal, TypeAlias
except ImportError:
    from typing_extensions import Final, Literal, TypeAlias


class IntPoint(NamedTuple):
    x: int
    y: int

IntPointLike: TypeAlias = "IntPoint | tuple[int, int]"

class Point(NamedTuple):
    x: float
    y: float

    def __add__(self, v: Vector | tuple[float, float]) -> Point:
        v = Vector(*v)
        return Point(self.x + v.dx, self.y + v.dy)
    
    def __mul__(self, n: float):
        return Point(self.x * n, self.y * n)
    
    # commutativity
    def __rmul__(self, n: float):
        return self * n
    
    @overload
    def __sub__(self, obj: Vector) -> Point: ...
    @overload
    def __sub__(self, obj: PointLike) -> Vector: ...
    def __sub__(self, obj: Vector | PointLike) -> Point | Vector:
        if isinstance(obj, Vector):
            return self + (-obj)
        else:
            obj = Point(*obj)
            return self.as_vector() - obj.as_vector()
    
    def __truediv__(self, n: float):
        return self * (1 / n)
    
    def __abs__(self):
        """magnitude"""
        return math.sqrt(self.x**2 + self.y**2)
    

    def as_vector(self) -> Vector:
        return Vector(*self)
    
    def round(self) -> IntPoint:
        return IntPoint(round(self.x), round(self.y))
    def floor(self) -> IntPoint:
        return IntPoint(math.floor(self.x), math.floor(self.y))
    def ceil(self) -> IntPoint:
        return IntPoint(math.ceil(self.x), math.ceil(self.y))

PointLike: TypeAlias = "Point | tuple[float, float]"

class Vector(NamedTuple):
    dx: float
    dy: float

    @overload
    def __add__(self, obj: Vector) -> Vector: ...
    @overload
    def __add__(self, obj: PointLike) -> Point: ...
    def __add__(self, obj: Vector | PointLike) -> Vector | Point:
        if isinstance(obj, Vector):
            return Vector(self.dx + obj.dx, self.dy + obj.dy)
        else:
            p = Point(*obj)
            return Point(self.dx + p.x, self.dy + p.y)
    
    def __mul__(self, n: float) -> Vector:
        return Vector(self.dx * n, self.dy * n)
    
    # commutativity
    def __rmul__(self, n: float) -> Vector:
        return self * n
    
    # must be left-multiplied
    def __rmatmul__(self, mat: tuple[tuple[float, float], tuple[float, float]]) -> Vector:
        return Vector(mat[0][0] * self.dx + mat[0][1] * self.dy, mat[1][0] * self.dx + mat[1][1] * self.dy)
    
    def __sub__(self, v: Vector) -> Vector:
        return self + (-v)
    
    def __truediv__(self, n: float) -> Vector:
        return self * (1 / n)
    
    def __abs__(self):
        """magnitude"""
        return math.sqrt(self.dx**2 + self.dy**2)
    
    def __neg__(self) -> Vector:
        return self * -1
    
    # positive rotation
    def __lshift__(self, angle: float) -> Vector:
        """rads"""
        return Vector.from_angle(self.get_angle() + angle) * abs(self)
    
    # negative rotation
    def __rshift__(self, angle: float) -> Vector:
        """rads"""
        return self << -angle
    

    def as_point(self) -> Point:
        return Point(*self)
    
    def get_angle(self) -> float:
        """rads"""
        return math.atan2(self.dy, self.dx)
    
    @staticmethod
    def from_angle(angle: float) -> Vector:
        """
        :param:`angle` rads

        Returns a unit vector in direction :param:`angle`.
        """
        return Vector(math.cos(angle), math.sin(angle))
    
    @staticmethod
    def from_polar(*, magnitude: float, angle: float) -> Vector:
        """
        :param:`angle` rads
        """
        return Vector.from_angle(angle) * magnitude
    
def make_linear_point_mapping(initial_points: tuple[PointLike, PointLike], final_points: tuple[PointLike, PointLike], mirror: bool = False) -> Callable[[Point], Point]:
    """see also lcd.lcd_make_coord_map"""
    o1 = Point(*initial_points[0])
    v1 = Point(*initial_points[1]) - o1
    v1_angle = v1.get_angle()

    o2 = Point(*final_points[0])
    v2 = Point(*final_points[1]) - o2

    rot_rads = v2.get_angle() - v1_angle
    scaling = abs(v2) / abs(v1)

    def f(p: Point) -> Point:
        # get vector from 'origin'
        v = p - o1

        if mirror:
            ang_diff_rads = v.get_angle() - v1_angle
            v = v >> 2 * ang_diff_rads

        # rotate and scale vector
        v = (v << rot_rads) * scaling

        # final position
        p_prime = o2 + v

        return p_prime
    
    return f

def make_coord_map(initial_points: tuple[PointLike, PointLike], final_points: tuple[PointLike, PointLike]) -> Callable[[Point], Point]:
    """
    Produces a function mapping initial_points to final_points via
    only stretches and translations to the x and y axis (independently).
    """
    initial_p1 = Point(*initial_points[0])
    initial_p2 = Point(*initial_points[1])
    initial_delta = initial_p2 - initial_p1

    final_p1 = Point(*final_points[0])
    final_p2 = Point(*final_points[1])
    final_delta = final_p2 - final_p1

    matrix = ((final_delta.dx / initial_delta.dx, 0), (0, -final_delta.dy / initial_delta.dy))

    def f(p: Point) -> Point:
        # get vector from p1 to p
        v = p - initial_p1

        # flip and scale
        v = matrix @ v

        # translate to screen coords
        p_prime = final_p1 + v

        return p_prime
    
    return f


from eye import RED, GREEN, BLUE, WHITE, GRAY, BLACK, ORANGE, SILVER, LIGHTGRAY, DARKGRAY, NAVY, CYAN, TEAL, MAGENTA, PURPLE, MAROON, YELLOW, OLIVE
Colour = int

def colour_to_str(col: Colour) -> str:
    return "#%0.6X" % col

def colour_to_tuple(col: Colour) -> tuple[int, int, int]:
    return (
        (col & 0xFF0000) // 0x010000,
        (col & 0x00FF00) // 0x000100,
        (col & 0x0000FF) // 0x000001
    )


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
    def from_list(image: Sequence[tuple[int, int, int]], *, gray: Literal[False] = False, resolution: ImageResolution) -> Image: ...

    @overload
    @staticmethod
    def from_list(image: Sequence[int], *, gray: Literal[True], resolution: ImageResolution) -> Image: ...

    @staticmethod
    def from_list(image: Sequence[tuple[int, int, int]] | Sequence[int], *, gray: bool = False, resolution: ImageResolution) -> Image:
        flat_image: Sequence[int]
        if not gray:
            image = cast("Sequence[tuple[int, int, int]]", image)
            flat_image = list(itertools.chain.from_iterable(image))
        else:
            flat_image = cast("Sequence[int]", image)
        c_bytes = (ctypes.c_byte * len(flat_image))(*flat_image)
        return Image(c_bytes, gray=gray, resolution=resolution)
    
    @staticmethod
    def from_colour_list(colour_image: Sequence[int], *, resolution: ImageResolution) -> Image:
        return Image.from_list(list(map(colour_to_tuple, colour_image)), gray=False, resolution=resolution)
    
    @overload
    def __getitem__(self, __key: int) -> int: ...
    @overload
    def __getitem__(self, __key: slice) -> list[int]: ...
    def __getitem__(self, *args):
        return self._c_bytes.__getitem__(*args)
    
    def __len__(self) -> int:
        return self._c_bytes.__len__()
    
    def get_gray(self, p: IntPointLike) -> int:
        p = IntPoint(*p)
        i = p.x + p.y * self.resolution.WIDTH
        return self[i]
    
    def get_colour(self, p: IntPointLike) -> tuple[int, int, int]:
        p = IntPoint(*p)
        i = (p.x + p.y * self.resolution.WIDTH) * 3
        return (self[i], self[i + 1], self[i + 2])
        ...
