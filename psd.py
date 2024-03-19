from __future__ import annotations

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


PSDPort = Literal[1, 2, 3, 4, 5, 6]
from eye import PSD_FRONT, PSD_LEFT, PSD_RIGHT, PSD_BACK

from eye import PSDGet as _PSDGet
def PSDGet(psd: PSDPort) -> int:
    """
    Returns the value of the sensor in mm.
    """
    return _PSDGet(psd)

from eye import PSDGetRaw as _PSDGetRaw
def PSDGetRaw(psd: PSDPort) -> int:
    """
    Bypasses the Hardware Description Table.
    Returns the raw value of the sensor.
    """
    return _PSDGetRaw(psd)
