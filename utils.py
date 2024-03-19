import math


def clamp(value: int, min_value: int, max_value: int) -> int:
    """
    Clamps the value within the min and max values, inclusive.
    """
    return max(min_value, min(max_value, value))

def wrap(value, min_value: int, max_value: int) -> int:
    """
    Wraps the value within the min and max values.
    :param:`max_value` will become :param:`min_value`.

    Examples:
    * `wrap(400, 0, 360)` => `40`
    * `wrap(180, -180, 180)` => `-180`
    """
    return (value - min_value) % (max_value - min_value) + min_value

def rad_to_deg(rads: float) -> float:
    return rads * 180 / math.pi

def deg_to_rad(degs: float) -> float:
    return degs * math.pi / 180
