from talon import Context, Module

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""

mod.list("cursorless_inside_outside", desc="Supported inside/outside types")
ctx.lists["self.cursorless_inside_outside"] = {
    "inner": "inside",
    "outer": "outside",
}


@mod.capture(rule="{user.cursorless_inside_outside}")
def cursorless_inside_outside(m) -> str:
    return {"insideOutsideType": m.cursorless_inside_outside}
