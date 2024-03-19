from typing import NamedTuple, overload

from eyepy.drawing import IntPoint, Point
from eyepy.motors import MOTORDrive
from eyepy.utils import wrap


def _VW_OK(return_code: int) -> bool:
    """
    Default VW return code checking behaviour
    """
    return return_code == 0

def wrap_turn_angle(angle: int) -> int:
    return wrap(angle, -180, 180)

from eye import VWSetSpeed as _VWSetSpeed
def VWSetSpeed(*, lin_speed: int, ang_speed: int) -> bool:
    """
    :param:`lin_speed` mm/s
    :param:`ang_speed` degrees/s

    Returns `True` if ok.
    """
    return_code = _VWSetSpeed(lin_speed, ang_speed)
    return _VW_OK(return_code)

# ? no VWGetSpeed
# ! TODO

class VWPosition(NamedTuple):
    pos: IntPoint
    """mm"""

    phi: int
    """degrees"""

    def as_float(self) -> tuple[Point, float]:
        return Point(*self.pos), self.phi

from eye import VWSetPosition as _VWSetPosition
@overload
def VWSetPosition(pos: VWPosition) -> bool: ...
@overload
def VWSetPosition(pos: IntPoint | tuple[int, int], phi: int) -> bool:
    """
    :param:`pos` mm
    :param:`phi` degrees

    Returns `True` if ok.
    """
    ...
def VWSetPosition(pos: VWPosition | IntPoint | tuple[int, int], phi: int | None = None) -> bool:
    """
    Returns `True` if ok.
    """
    if isinstance(pos, VWPosition):
        pos, phi = pos
    pos = IntPoint(*pos)
    return_code = _VWSetPosition(pos.x, pos.y, phi)
    return _VW_OK(return_code)

from eye import VWGetPosition as _VWGetPosition
def VWGetPosition() -> VWPosition:
    x, y, phi = _VWGetPosition()
    return VWPosition(IntPoint(x, y), phi)

from eye import VWStraight as _VWStraight
def VWStraight(dist: int, *, lin_speed: int) -> bool:
    """
    :param:`dist` mm
    :param:`lin_speed` mm/s

    Returns `True` if ok.
    """
    return_code = _VWStraight(dist, lin_speed)
    return _VW_OK(return_code)

from eye import VWTurn as _VWTurn
def VWTurn(angle: int, *, ang_speed: int, wrap: bool = True) -> bool:
    """
    :param:`angle` degrees
    :param:`ang_speed` degrees/s
    :param:`wrap` if `True`, turns the shortest distance; wraps values from -180 to 180

    Returns `True` if ok.
    """
    if wrap:
        angle = wrap_turn_angle(angle)
    
    return_code = _VWTurn(angle, ang_speed)
    return _VW_OK(return_code)

from eye import VWCurve as _VWCurve
def VWCurve(*, dist: int, angle: int, lin_speed: int, wrap: bool = True) -> bool:
    """
    :param:`dist` mm
    :param:`angle` degrees (orientation change)
    :param:`lin_speed` mm/s
    :param:`wrap` if `True`, turns the shortest distance; wraps values from -180 to 180

    Returns `True` if ok.
    """
    if wrap:
        angle = wrap_turn_angle(angle)

    return_code = _VWCurve(dist, angle, lin_speed)
    return _VW_OK(return_code)

from eye import VWDrive as _VWDrive
def VWDrive(*, dx: int, dy: int, lin_speed: int) -> bool:
    """
    :param:`dx` mm
    :param:`dy` mm
    :param:`lin_speed` mm/s

    `x` must be greater than the magnitude of `y`.

    Returns `True` if ok.
    """
    # ! TODO check if should throw exception if x <= |y|
    return_code = _VWDrive(dx, dy, lin_speed)
    return _VW_OK(return_code)

from eye import VWRemain as _VWRemain
def VWRemain() -> int:
    """
    Returns the remaining drive distance in mm.
    """
    return _VWRemain()

from eye import VWDone as _VWDone
def VWDone() -> bool:
    """
    Returns whether the drive is finished (non-blocking).
    """
    return _VWDone() == 1

from eye import VWWait as _VWWait
def VWWait() -> bool:
    """
    Suspends the current thread until drive operation has finished.
    
    Returns `True` if ok.
    """
    return_code = _VWWait()
    return _VW_OK(return_code)

from eye import VWStalled as _VWStalled
def VWStalled() -> tuple[bool, bool]:
    """
    Returns the stall state of the left and right motors (motors 1 and 2) respectively.
    `True` means stalled.
    """
    state: int = _VWStalled()
    left_stalled = (state & 0b01) != 0
    right_stalled = (state & 0b10) != 0
    return left_stalled, right_stalled


# extra funcs

def VWStop() -> bool:
    return MOTORDrive([1, 2], 0)
