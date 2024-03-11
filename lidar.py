from typing import NamedTuple, Optional


_lidar_range = 360
_lidar_tilt = 0
_lidar_n_points = 360

from eye import LIDARGet as _LIDARGet
def LIDARGet(*, range: Optional[int] = None, tilt: Optional[int] = None, n_points: Optional[int] = None) -> list[int]:
    """
    Returns distances in mm.
    Default range is 360 degrees and 360 points, unless modified using :func:`LIDARSet`.
    Any LIDAR config values passed in will have precedence over the current global LIDAR config.
    """
    if all(value is None for value in [range, tilt, n_points]):
        # no config changed; no extra logic needed
        return list(_LIDARGet())

    # save current config
    old_range = _lidar_range
    old_tilt = _lidar_tilt
    old_n_points = _lidar_n_points

    LIDARSet(range=range, tilt=tilt, n_points=n_points)
    distances: list[int] = list(_LIDARGet())

    # restore current config
    LIDARSet(range=old_range, tilt=old_tilt, n_points=old_n_points)

    return distances

from eye import LIDARSet as _LIDARSet
def LIDARSet(*, range: Optional[int] = None, tilt: Optional[int] = None, n_points: Optional[int] = None):
    """
    Updates the global LIDAR config.
    Any values set to `None` will keep their current values.

    :param:`range` degrees, centred forwards
    :param:`tilt` degrees, positive downwards
    :param:`n_points` the number of point in and returned by the scan
    """
    global _lidar_range
    global _lidar_tilt
    global _lidar_n_points

    if range is not None:
        _lidar_range = range
    
    if tilt is not None:
        _lidar_tilt = tilt
    
    if n_points is not None:
        _lidar_n_points = n_points

class LIDARConfig(NamedTuple):
    range: int
    """degrees, centred forwards"""

    tilt: int
    """degrees, positive downwards"""

    n_points: int
    """the number of point in and returned by the scan"""

def LIDARGetConfig() -> LIDARConfig:
    return LIDARConfig(range=_lidar_range, tilt=_lidar_tilt, n_points=_lidar_n_points)
