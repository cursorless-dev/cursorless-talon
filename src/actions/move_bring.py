from ..primitive_target import STRICT_HERE
from talon import Context, Module

mod = Module()

ctx = Context()
ctx.matches = r"""
tag: user.cursorless
"""


mod.list("cursorless_move_bring_action", desc="Cursorless move or bring actions")
ctx.lists["self.cursorless_move_bring_action"] = {"bring", "move"}


@mod.capture(rule=("<user.cursorless_target> [to <user.cursorless_target>]"))
def cursorless_move_bring_targets(m) -> str:
    target_list = m.cursorless_target_list

    if len(target_list) == 1:
        target_list = target_list + [STRICT_HERE]

    return target_list
