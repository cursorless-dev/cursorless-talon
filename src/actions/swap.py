from talon import Module
from ..primitive_target import BASE_TARGET

mod = Module()

mod.list("cursorless_swap_action", desc="Cursorless swap action")


@mod.capture(
    rule=(
        "{user.cursorless_swap_action} [<user.cursorless_target>] with <user.cursorless_target>"
    )
)
def cursorless_swap(m) -> str:
    target_list = m.cursorless_target_list

    if len(target_list) == 1:
        target_list = [BASE_TARGET] + target_list

    return target_list
