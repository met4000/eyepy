def _MOTOR_OK(return_code: int) -> bool:
    """
    Default motor return code checking behaviour
    """
    return return_code == 0

MotorPort = Literal[1] | Literal[2] | Literal[3] | Literal[4] # ! TODO any?

from typing import Literal
from eye import MOTORDrive as _MOTORDrive
def MOTORDrive(*, motor: MotorPort, speed: int) -> bool:
    """
    :param:`motor`
    :param:`speed` percentage speed (-100 - 100)

    Returns `True` if ok.
    """
    return_code = _MOTORDrive(lin_speed, ang_speed)
    return _MOTOR_OK(return_code)