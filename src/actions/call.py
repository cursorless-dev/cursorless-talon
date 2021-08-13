from ..primitive_target import STRICT_HERE
from talon import Module

mod = Module()


@mod.capture(rule=("call <user.cursorless_target> [on <user.cursorless_target>]"))
def cursorless_call(m) -> str:
    target_list = m.cursorless_target_list

    if len(target_list) == 1:
        target_list = target_list + [STRICT_HERE]

    return target_list
