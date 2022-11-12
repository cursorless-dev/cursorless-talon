# from talon import Module

from contextlib import suppress
from ..primitive_target import BASE_TARGET

def cursorless_swap_targets(m) -> list[dict]:
    target_list = [m["target2"]]
    with suppress(KeyError):
        target_list.append(m["target1"])

    if len(target_list) == 1:
        target_list = [BASE_TARGET] + target_list

    return target_list
