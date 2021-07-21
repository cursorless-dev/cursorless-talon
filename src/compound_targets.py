from .primitive_target import BASE_TARGET
from talon import Module

mod = Module()


@mod.capture(
    rule=(
        "<user.cursorless_primitive_target> | "
        "(past|till|tween) <user.cursorless_primitive_target> | "
        "<user.cursorless_primitive_target> (past|till|tween) <user.cursorless_primitive_target>"
    )
)
def cursorless_range(m) -> str:
    length = len(m)
    if length == 1:
        return m[0]

    if length == 2:
        start = BASE_TARGET.copy()
    else:
        start = m[0]
    modifier = m[-2]
    return {
        "type": "range",
        "start": start,
        "end": m[-1],
        "excludeStart": modifier == "tween",
        "excludeEnd": modifier in ["tween", "till"],
    }


@mod.capture(rule=("<user.cursorless_range> (and <user.cursorless_range>)*"))
def cursorless_target(m) -> str:
    if len(m.cursorless_range_list) == 1:
        return m.cursorless_range
    return {"type": "list", "elements": m.cursorless_range_list}
