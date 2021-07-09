from .primitive_target import BASE_TARGET
from talon import Module

mod = Module()


@mod.capture(
    rule=(
        "<user.cursorless_primitive_target> | "
        "past <user.cursorless_primitive_target> | "
        "<user.cursorless_primitive_target> past <user.cursorless_primitive_target>"
    )
)
def cursorless_range(m) -> str:
    if "past" in m:
        end = m[-1]
        if m[0] == "past":
            start = BASE_TARGET.copy()
        else:
            start = m.cursorless_primitive_target_list[0]
        return {
            "type": "range",
            "start": start,
            "end": end,
        }

    return m[0]


@mod.capture(rule=("<user.cursorless_range> (and <user.cursorless_range>)*"))
def cursorless_target(m) -> str:
    if len(m.cursorless_range_list) == 1:
        return m.cursorless_range
    return {
        "type": "list",
        "elements": m.cursorless_range_list
    }
