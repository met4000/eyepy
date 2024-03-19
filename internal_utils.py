from typing import Callable, TypeVar


T = TypeVar("T")
R = TypeVar("R")
def repeat_func(inputs: T | list[T], func: Callable[[T], R], ok_predicate: Callable[[R], bool]) -> bool:
    input_list: list[T] = inputs if isinstance(inputs, list) else [inputs]
    return_codes = [func(input) for input in input_list]
    return all(ok_predicate(code) for code in return_codes)
