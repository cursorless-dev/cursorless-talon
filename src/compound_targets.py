from .primitive_target import BASE_TARGET
from talon import Module, Context

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""

range_specifier = {
    "past",
    "until",
    "tween",
}

mod.list("cursorless_range_specifier", desc="A symbol that comes in pairs, eg brackets")
ctx.lists["self.cursorless_range_specifier"] = range_specifier


@mod.capture(
    rule=(
        "[{user.cursorless_range_specifier}] <user.cursorless_primitive_target> | "
        "<user.cursorless_primitive_target> {user.cursorless_range_specifier} <user.cursorless_primitive_target>"
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
        "excludeEnd": modifier in ["tween", "until"],
    }


@mod.capture(rule="<user.cursorless_range> (and <user.cursorless_range>)*")
def cursorless_target(m) -> str:
    if len(m.cursorless_range_list) == 1:
        return m.cursorless_range
    return {"type": "list", "elements": m.cursorless_range_list}
