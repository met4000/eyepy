from typing import Callable, Literal, TypeVar


T = TypeVar("T")
R = TypeVar("R")
def _repeat_func(inputs: T | list[T], func: Callable[[T], R], ok_predicate: Callable[[R], bool]) -> bool:
    input_list: list[T] = inputs if isinstance(inputs, list) else [inputs]
    return_codes = [func(input) for input in input_list]
    return all(ok_predicate(code) for code in return_codes)

def clamp(value: int, min_value: int, max_value: int) -> int:
    """
    Clamps the value within the min and max values, inclusive.
    """
    return max(min_value, min(max_value, value))

# SERVOS

def _SERVO_OK(return_code: int) -> bool:
    """
    Default servo return code checking behaviour.
    """
    return return_code == 0

ServoPort = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

def clamp_servo_angle(angle: int, *, no_zero = False) -> int:
    """
    Clamps the value to within the minimum and maximum servo angle values.

    :param:`no_zero` if `True`, `0` will not be included as a valid value
    """
    return clamp(angle, 1 if no_zero else 0, 255)

from eye import SERVOSet as _SERVOSet
def SERVOSet(servos: ServoPort | list[ServoPort], angle: int, *, clamp_angle = False) -> bool:
    """
    :param:`servos` the servo(s) to set
    :param:`angle` angle (1 to 255) or power down (0)
    Note: the docs specify 0 as power down, but in the sim it seems to be a valid angle

    :param:`clamp_angle` if `True` uses :func:`clamp_servo_angle` to clamp :param:`angle`

    Returns `True` if all ok.
    """
    if clamp_angle:
        angle = clamp_servo_angle(angle)
    
    if angle < 0 or angle > 255:
        raise ValueError(f"angle value out of bounds; expected a value from 0 to 255 but got: {angle}")
    
    return _repeat_func(servos, lambda servo: _SERVOSet(servo, angle), _SERVO_OK)

from eye import SERVOSetRaw as _SERVOSetRaw
def SERVOSetRaw(servos: ServoPort | list[ServoPort], angle: int, *, clamp_angle = False) -> bool:
    """
    Bypasses the Hardware Description Table.

    :param:`servos` the servo(s) to set
    :param:`angle` angle (0 or 1 to 255)
    Note: the docs specify 0 as power down in :func:`SERVOSet`, but in the sim it seems to be a valid angle

    :param:`clamp_angle` if `True` uses :func:`clamp_servo_angle` to clamp :param:`angle`

    Returns `True` if all ok.
    """
    if clamp_angle:
        angle = clamp_servo_angle(angle)
    
    if angle < 0 or angle > 255:
        raise ValueError(f"angle value out of bounds; expected a value from 0 to 255 but got: {angle}")
    
    return _repeat_func(servos, lambda servo: _SERVOSetRaw(servo, angle), _SERVO_OK)

from eye import SERVORange as _SERVORange
def SERVORange(servos: ServoPort | list[ServoPort], low: int, high: int) -> bool:
    """
    "Set servo limits in 1/100 sec"

    :param:`servos` the servo(s) to set
    :param:`low`
    :param:`high`
    TODO: determine what this function does

    Returns `True` if all ok.
    """
    return _repeat_func(servos, lambda servo: _SERVORange(servo, low, high), _SERVO_OK)


# MOTORS

def _MOTOR_OK(return_code: int) -> bool:
    """
    Default motor return code checking behaviour.
    """
    return return_code == 0

def clamp_motor_speed(speed: int) -> int:
    return clamp(speed, -100, 100)

MotorPort = Literal[1, 2, 3, 4]

from eye import MOTORDrive as _MOTORDrive
def MOTORDrive(motors: MotorPort | list[MotorPort], speed: int, *, clamp_speed = False) -> bool:
    """
    :param:`motor` the motor(s) to drive
    :param:`speed` percentage speed (clamped within -100 to 100)
    :param:`clamp_speed` if `True` uses :func:`clamp_motor_speed` to clamp :param:`speed`

    Returns `True` if all ok.
    """
    if clamp_speed:
        speed = clamp_motor_speed(speed)
    
    if speed < -100 or speed > 100:
        raise ValueError(f"speed value out of bounds; expected a value from -100 to 100 but got: {speed}")
    
    return _repeat_func(motors, lambda motor: _MOTORDrive(motor, speed), _MOTOR_OK)

from eye import MOTORDriveRaw as _MOTORDriveRaw
def MOTORDriveRaw(motors: MotorPort | list[MotorPort], speed: int, *, clamp_speed = False) -> bool:
    """
    Bypasses the Hardware Description Table.

    :param:`motor` the motor(s) to drive
    :param:`speed` percentage speed (clamped within -100 to 100)
    :param:`clamp_speed` if `True` uses :func:`clamp_motor_speed` to clamp :param:`speed`

    Returns `True` if all ok.
    """
    if clamp_speed:
        speed = clamp_motor_speed(speed)
    
    if speed < -100 or speed > 100:
        raise ValueError(f"speed value out of bounds; expected a value from -100 to 100 but got: {speed}")
    
    return _repeat_func(motors, lambda motor: _MOTORDriveRaw(motor, speed), _MOTOR_OK)

# MotorPIDOutOfBounds

from eye import MOTORPID as _MOTORPID
def MOTORPID(motors: MotorPort | list[MotorPort], p: int, i: int, d: int) -> bool:
    """
    :param:`motor` the motor(s) to set the PID controller values on
    :param:`p`, :param:`i`, :param:`d` the values to set (0 to 255)
    Note: the docs specify 1..255 but 0 seems ok?

    Throws a `ValueError` if the PID controller values are out of bounds.

    Returns `True` if all ok.
    """
    for v in [p, i, d]:
        if v < 0 or v > 255:
            raise ValueError(f"PID controller values out of bounds; expected values from 0 to 255 but got p: {p}, i: {i}, d: {d}")
    
    return _repeat_func(motors, lambda motor: _MOTORPID(motor, p, i, d), _MOTOR_OK)

from eye import MOTORPIDOff as _MOTORPIDOff
def MOTORPIDOff(motors: MotorPort | list[MotorPort]) -> bool:
    """
    :param:`motor` the motor(s) to drive

    Returns `True` if all ok.
    """
    return _repeat_func(motors, lambda motor: _MOTORPIDOff(motor), _MOTOR_OK)

from eye import MOTORSpeed as _MOTORSpeed
def MOTORSpeed(motors: MotorPort | list[MotorPort], ticks: int) -> bool:
    """
    :param:`motor` the motor(s) to drive
    :param:`ticks` ticks per 100 sec

    Returns `True` if all ok.
    """
    return _repeat_func(motors, lambda motor: _MOTORSpeed(motor, ticks), _MOTOR_OK)


# ENCODERS

EncoderPort = MotorPort

from eye import ENCODERRead as _ENCODERRead
def ENCODERRead(encoder: EncoderPort) -> int:
    return _ENCODERRead(encoder)

from eye import ENCODERReset as _ENCODERReset
def ENCODERReset(encoder: EncoderPort) -> bool:
    """
    TODO check the return value; currently assumes `0` is non-error, and any other value implies a failure

    Returns `True` if ok.
    """
    return_code = _ENCODERReset(encoder)
    return return_code == 0
